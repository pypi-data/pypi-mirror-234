import sys
import os
import datetime
from concurrent.futures import ThreadPoolExecutor

from importlib import import_module
from pathlib import Path
from argparse import ArgumentParser

import httpx
from colorama import Fore

from aw_client.models.model_schema import ModelObject, ModelSchema
from aw_client.session import Session

from aw_client.model_dev.cache import ModelDevCache
from aw_client.model_dev.application import Application
from aw_client.model_dev.virtual_objects import get_virtual_object_dataframe


try:
    import pyspark
    from pyspark.sql import SparkSession
    from pyspark.sql.types import StringType, LongType, DateType, TimestampType
    import pyspark.sql.functions as F
except ImportError:
    raise Exception('Для запуска скрипта модели необходимо установить библиотеку pyspark')


# ----------------------------------------------------------------------------------------------------------------------
# UDF функции
# ----------------------------------------------------------------------------------------------------------------------
def udf_aw_mask(text, mask_symb, pos):
    """ """
    return None if text is None else (mask_symb*pos + text[pos:])[:len(text)]


def udf_aw_cast_interval(dt_start: datetime.datetime, dt_finish: datetime.datetime, measure="sec"):
    """
    Возвращает интервал между двумя временными значениями (dt_finish - dt_start)
    в единицах, заданных параметром measure: [days|hours|minutes|sec|ms].
    В случае, если хотя бы одна из границ периода передана как None, возвращается None.
    В случае, если measure имеет недопустимое значение, возвращается None.
    """

    if dt_start is None or dt_finish is None:
        return None

    if not isinstance(dt_start, datetime.datetime):
        dt_start = datetime.datetime.combine(dt_start, datetime.time.min)

    if not isinstance(dt_finish, datetime.datetime):
        dt_finish = datetime.datetime.combine(dt_finish, datetime.time.min)

    delta = dt_finish - dt_start

    try:
        if measure == "days":
            return delta.days
        elif measure == "hours":
            return delta.days * 24 + delta.seconds // 3600
        elif measure == "minutes":
            return delta.days * 24 * 60 + delta.seconds // 60
        elif measure == "sec":
            return delta.days * 24 * 3600 + delta.seconds
        elif measure == "ms":
            return (delta.days * 24 * 3600 + delta.seconds) * 1000 + delta.microseconds // 1000
        else:
            return None
    except OverflowError:
        return None


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('file', type=str)
    parser.add_argument('--aw-url', dest='aw_url', type=str, required=True)
    parser.add_argument('--aw-token', dest='aw_token', type=str, required=True)
    parser.add_argument('--no-cache', dest='no_cache', action='store_true', default=False, required=False)
    parser.add_argument('--full', dest='full', action='store_true',  default=False, required=False)
    parser.add_argument('--cores', dest='cores', type=int, default=None)

    args, _ = parser.parse_known_args()

    script_path = Path(args.file)

    try:
        model_id = int(script_path.stem[6:])
    except Exception as e:
        print(Fore.RED + f'Не получить номер модели из названия файла {script_path}. '
                         f'Имя файла должно быть вида model_NNN.py, где вместо NNN ожидается идентификатор '
                         f'модели (например, model_123.py)')
        sys.exit(1)

    # Импортируем указанный файл
    print('--------------------------------------------------------------')
    print(f'Запускается ETL-скрипт с параметрами:')
    print(f'  - model_id: {model_id}')
    print(f'  - file: {script_path}')
    print(f'  - AW url: {args.aw_url}')
    print(f'  - Кеш данных: {"нет" if args.no_cache else "да"}')
    print(f'  - Полный набор данных из источника: {"да" if args.full else "нет"}')
    print(f'  - Использовать ядра: {"все" if args.cores is None else args.cores}')
    print('--------------------------------------------------------------\n')
    sys.path.insert(0, Path(args.file).parent.as_posix())
    etl_script_module = import_module(Path(args.file).stem)

    # Сессия для работы с AW
    session = Session(aw_url=args.aw_url, token=args.aw_token)

    try:
        if session.get_aw_version() < 2:
            print(Fore.RED + 'Версия AW должна быть как минимум 1.19' + Fore.RESET)
            sys.exit(-1)
    except httpx.HTTPError as e:
        print(Fore.YELLOW + f'Не удалось проверить версию AW на актуальность: {e}' + Fore.RESET)

    # Работа
    cache = ModelDevCache(
        cache_root_folder=Path(args.file).parent / '.aw-cache', aw_url=args.aw_url, model_id=model_id,
        is_full=args.full)

    # Сессия спарка
    master_url = 'local'
    if args.cores is not None:
        master_url = f'local[{args.cores}]'
    else:
        master_url = 'local[*]'
    spark = SparkSession.builder.config("spark.driver.host", "127.0.0.1").master(master_url).appName(f'model_{model_id}').getOrCreate()
    spark.sparkContext.setLogLevel('WARN')

    spark.udf.register('awmask', udf_aw_mask, StringType())
    spark.udf.register('awcastinterval', udf_aw_cast_interval, LongType())

    spark.conf.set('spark.sql.caseSensitive', False)
    spark.conf.set('spark.sql.files.maxPartitionBytes', 10000000)
    spark.conf.set('spark.sql.parquet.outputTimestampType', 'TIMESTAMP_MILLIS')
    spark.conf.set('spark.sql.parquet.datetimeRebaseModeInRead', 'CORRECTED')
    spark.conf.set('spark.sql.parquet.mergeSchema', 'true')
    spark.conf.set('spark.sql.parquet.datetimeRebaseModeInWrite', 'CORRECTED')

    # ------------------------------------------------------------------------------
    # Загрузка схемы модели
    # ------------------------------------------------------------------------------
    print('Загрузка схемы модели из AW... ', end=' ')
    try:
        model_schema = session.model_schema(model_id)
    except httpx.HTTPError as e:
        if cache.model_schema_path().exists() and not args.no_cache:
            print(Fore.YELLOW + f'Не удалось получить схему модели {model_id}: {e}. '
                                f'Для запуска скрипта используется схема модели из кеша.' + Fore.RESET)
            model_schema = ModelSchema.parse_file(cache.model_schema_path())
        else:
            print(Fore.RED + f'ОШИБКА: Не удалось получить схему модели {model_id}: {e}' + Fore.RESET)
            sys.exit(1)
    except Exception as e:
        print(Fore.RED + f'ОШИБКА: Не удалось получить схему модели {model_id}: {e}' + Fore.RESET)
        sys.exit(1)
    print(Fore.GREEN + 'OK' + Fore.RESET)

    cache_folder = cache.get_model_folder()
    os.makedirs(cache_folder, exist_ok=True)
    with open(cache.model_schema_path(), 'wt') as f:
        f.write(model_schema.json(ensure_ascii=False, indent=2))

    # ------------------------------------------------------------------------------
    # Загрузка данных объектов модели
    # ------------------------------------------------------------------------------
    def load_object_data(model_object: ModelObject, use_cache: bool):
        if cache.model_object_data_folder(model_object.model_name).exists() and use_cache and \
                cache.is_model_object_actual(model_object):
            print(Fore.RESET + f'Данные для {model_object.model_name} - ' + Fore.GREEN + 'OK (из кеша)' + Fore.RESET)
        else:
            print(Fore.RESET + f'Получение данных объекта {model_object.model_name} из AW ... ')
            try:
                session.load_model_object_data(folder=cache.model_source_folder(),
                                               model_id=model_id,
                                               model_object_name=model_object.model_name,
                                               limit=None if args.full else 10_000)
            except Exception as e:
                print(Fore.RED + f'Ошибка загрузки данных для {model_object.model_name}: {e}' + Fore.RESET)
                raise

            # сохраняем хеш для кешированных данных
            cache.set_model_object_hash(model_object)
            print(Fore.RESET + f'Данные для {model_object.model_name} - ' + Fore.GREEN + 'OK ' + Fore.RESET)
        return True

    with ThreadPoolExecutor(max_workers=4) as executor:
        non_virtual_objects = [o for o in model_schema.objects if o.type != 'virtual']
        for model_obj, obj_result in zip(non_virtual_objects, executor.map(
                lambda model_object: load_object_data(model_object, use_cache=not args.no_cache),
                non_virtual_objects
        )):
            if not obj_result:
                sys.exit(1)

    application = Application()
    # ------------------------------------------------------------------------------
    # Выполняем before_all
    # ------------------------------------------------------------------------------
    if hasattr(etl_script_module, 'before_all'):
        print(Fore.GREEN + 'Выполняется before_all(..)' + Fore.RESET)
        getattr(etl_script_module, 'before_all')(application, spark)

    # ------------------------------------------------------------------------------
    # Загрузка объектов модели
    # ------------------------------------------------------------------------------
    source_dfs = {}
    for model_object in model_schema.objects:
        if model_object.type == 'virtual':
            source_dfs[model_object.model_name] = get_virtual_object_dataframe(spark=spark, model_object=model_object)
        elif model_schema.sql.xsqls and model_object.model_name in model_schema.sql.xsqls:
            xsql = model_schema.sql.xsqls[model_object.model_name].replace('%WHERE%', '').replace(
                "%RUN_FOLDER%", cache.model_source_folder().as_posix())
            source_dfs[model_object.model_name] = spark.sql(xsql)
        else:
            try:
                source_dfs[model_object.model_name] = spark.read.parquet(
                    (cache.model_source_folder() / f'{model_object.model_name}.parquet').as_posix())
            except Exception as e:
                print(Fore.YELLOW + f'Не удалось загрузить данные для {model_object.model_name}: {e}' + Fore.RESET)
                # Молча проглотим ошибку, т.к. этот датафрейм может и не пригодиться в работе. Иначе,
                # возникнет ошибка ниже
                pass

    # ------------------------------------------------------------------------------
    # Выполняем функции из etl-скрипта
    # ------------------------------------------------------------------------------
    for model_object in model_schema.objects:
        method_name = f'after_load_{model_object.model_name}'
        if hasattr(etl_script_module, method_name) and model_object.model_name in source_dfs:
            print(Fore.GREEN + f'Выполняется after_load_{model_object.model_name}(..)' + Fore.RESET)
            source_dfs[model_object.model_name] = getattr(etl_script_module, method_name)(
                df=source_dfs[model_object.model_name],
                app=application,
                spark=spark
            )
            if not isinstance(source_dfs[model_object.model_name], pyspark.sql.DataFrame):
                raise Exception(f'Функция {method_name} должна вернуть объект типа pyspark.sql.DataFrame')

    # ------------------------------------------------------------------------------
    # Регистрация датафреймов из источников в spark-окружении
    # ------------------------------------------------------------------------------
    for obj_name, df in source_dfs.items():
        df.createOrReplaceTempView(obj_name)

    # ------------------------------------------------------------------------------
    # Выполняем итоговый SQL
    # ------------------------------------------------------------------------------
    print(Fore.GREEN + 'Выполняется итоговый SQL' + Fore.RESET)
    sql = model_schema.sql.sql.replace('parquet.`%RUN_FOLDER%/', '').replace('.parquet`', '').replace('%WHERE%', '')
    df_final = spark.sql(sql)

    # ------------------------------------------------------------------------------
    # Выполняем after_all
    # ------------------------------------------------------------------------------
    if hasattr(etl_script_module, 'after_all'):
        print(Fore.GREEN + 'Выполняется after_all(..)' + Fore.RESET)
        df_final = getattr(etl_script_module, 'after_all')(
            df=df_final,
            app=application,
            spark=spark
        )

    # ------------------------------------------------------------------------------
    # Конец
    # ------------------------------------------------------------------------------
    print(Fore.GREEN + 'ETL-скрипт успешно выполнен.' + Fore.RESET)
