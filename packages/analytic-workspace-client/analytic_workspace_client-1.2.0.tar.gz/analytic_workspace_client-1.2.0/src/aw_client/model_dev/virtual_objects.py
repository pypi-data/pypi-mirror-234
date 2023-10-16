from pathlib import Path

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.types import StructType, StructField, DataType, LongType, DoubleType, TimestampType, StringType, \
        BooleanType
except ImportError:
    raise Exception('Для запуска скрипта модели необходимо установить библиотеку pyspark')

from aw_client.models.model_schema import ModelObject


def get_virtual_object_dataframe(spark: SparkSession, model_object: ModelObject):
    """ """

    if not model_object.fields:
        raise Exception(f'Поля для виртуального объекта {model_object.model_name} не заданы')

    schema_fields = []
    for field in model_object.fields:
        schema_fields.append(
            StructField(
                name=field.model_name,
                dataType=get_spark_type_for_simple_type(field.simple_type),
                nullable=True
            )
        )

    return spark.createDataFrame(data=[], schema=StructType(schema_fields))


def get_spark_type_for_simple_type(simple_type: str) -> DataType:
    """ """
    if simple_type == 'number':
        return LongType()
    elif simple_type == 'float':
        return DoubleType()
    elif simple_type == 'date':
        return TimestampType()
    elif simple_type == 'bool':
        return BooleanType()
    else:
        return StringType()
