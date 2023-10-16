from typing import Optional
from pathlib import Path

import pandas

from aw_client.data_master.base import DataMasterApi
from aw_client.exceptions import WrongDataMasterApiVersion
from aw_client.models.model_schema import ModelSchema
from aw_client.tools import get_temp_folder


class DataMasterV1(DataMasterApi):
    """ """
    def load_model(self, model_id: int, **options) -> pandas.DataFrame:
        """ """
        apply_schema = options.get('schema')
        if apply_schema is None:
            apply_schema = True

        timeout = options.get('timeout')
        if timeout is not None:
            timeout = int(timeout)

        with self.get_http_client() as client:

            model_schema = None
            if apply_schema:
                model_schema = client.get('data-master/v1/model/schema', params={'model_id': model_id}).json()

            with get_temp_folder() as temp_folder:
                temp_file = temp_folder / 'model_data.json'
                params = {'model_id': model_id, 'format': 'json-lines'}
                with client.stream(method='GET', url='data-master/v1/model/data', params=params, timeout=timeout) as r:
                    if not r.is_success:
                        r.read()
                        raise DataMasterApi.Error(f'Ошибка запроса GET {r.url}: HTTP {r.status_code}: {r.text}')
                    with open(temp_file, 'wb') as f:
                        for chunk in r.iter_bytes():
                            f.write(chunk)

                    df = pandas.read_json(temp_file, lines=True)

        if apply_schema:
            as_type = {}

            for column in model_schema['fields']:
                # if column['simple_type'] == 'string':
                #     as_type[column['model_name']] = 'object'
                # elif column['simple_type'] == 'number':
                #     as_type[column['model_name']] = 'int64'
                # elif column['simple_type'] == 'float':
                #     as_type[column['model_name']] = 'float64'
                # elif column['simple_type'] == 'bool':
                #     as_type[column['model_name']] = 'bool'
                if column['simple_type'] == 'date':
                    as_type[column['model_name']] = 'datetime64[ns]'

            df = df.astype(as_type)

        return df

    def model_schema(self, model_id: int) -> ModelSchema:
        raise WrongDataMasterApiVersion(f'Получение схемы модели доступно для Analytic Workspace с версии 1.19')

    def load_model_object_data(self, folder: Path, model_id: int, model_object_name: str, limit: Optional[int]):
        """ """
        raise WrongDataMasterApiVersion(f'Получение данных объекта модели доступно для AW с версии 1.19')
