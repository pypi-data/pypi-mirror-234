import shutil
from typing import Optional

from pathlib import Path

import pandas

from aw_client.data_master import DataMasterApi
from aw_client.domain import APIConfig
from aw_client.models.model_schema import ModelSchema

from .v1 import DataMasterV1
from ..exceptions import AwModelForbidden
from ..tools import get_temp_folder


class DataMasterV2(DataMasterApi):
    """ """
    def __init__(self, api_config: APIConfig):
        super().__init__(api_config)

        self.api_config = api_config
        self.api_v1 = DataMasterV1(api_config)  # это не очень хорошо, но пока идей нет, как лучше сделать

    def load_model(self, model_id: int, **options) -> pandas.DataFrame:
        return self.api_v1.load_model(model_id, **options)

    def model_schema(self, model_id: int) -> ModelSchema:
        """ """
        with self.get_http_client() as client:
            r = client.get(url='data-master/v2/model/schema', params={'model_id': model_id})
            if not r.is_success:
                if r.status_code == 403:
                    raise AwModelForbidden(f'Доступ к модели {model_id} запрещен')
                raise Exception(f'Ошибка запроса схемы модели HTTP {r.status_code} GET {r.url}: {r.text}')

            return ModelSchema.parse_obj(r.json())

    def load_model_object_data(self, folder: Path, model_id: int, model_object_name: str, limit: Optional[int]):
        """ """
        with self.get_http_client() as client:
            params = {
                'model_id': model_id,
                'model_object_name': model_object_name
            }
            if limit is not None:
                params['limit'] = limit

            with get_temp_folder() as temp_folder:
                temp_file = temp_folder / f'{model_object_name}.zip'
                with client.stream(method='GET', url='data-master/v2/model-object/data', params=params, timeout=None) as r:
                    if not r.is_success:
                        r.read()
                        raise DataMasterApi.Error(f'Ошибка запроса GET {r.url}: HTTP {r.status_code}: {r.text}')
                    else:
                        with open(temp_file, 'wb') as f:
                            for chunk in r.iter_bytes():
                                f.write(chunk)

                if (folder / f'{model_object_name}.parquet').exists():
                    shutil.rmtree(folder / f'{model_object_name}.parquet')

                shutil.unpack_archive(temp_file, folder.as_posix())

        return
