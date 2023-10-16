from typing import Optional
from pathlib import Path
import pandas
import io

from aw_client.data_master.base import DataMasterApi
from aw_client.exceptions import WrongDataMasterApiVersion
from aw_client.models.model_schema import ModelSchema


class DataMasterV0(DataMasterApi):
    """ """

    def load_model(self, model_id: int, **options) -> pandas.DataFrame:
        """ """
        with self.get_http_client() as client:
            url = f"data-master/v0/model/data?model_id={model_id}&format=csv"
            r = client.get(url, timeout=None)
            if not r.is_success:
                raise Exception(f"Ошибка загрузки данных модели: {r.text}")

        return pandas.read_csv(io.StringIO(r.content.decode("utf-8")))

    def model_schema(self, model_id: int) -> ModelSchema:
        raise WrongDataMasterApiVersion(f'Получение схемы модели доступно для AW с версии 1.19')

    def load_model_object_data(self, folder: Path, model_id: int, model_object_name: str, limit: Optional[int]):
        """ """
        raise WrongDataMasterApiVersion(f'Получение данных объекта модели доступно для AW с версии 1.19')
