from typing import Optional

import abc
from pathlib import Path

import pandas
import httpx

from contextlib import contextmanager

from aw_client.models.model_schema import ModelSchema
from aw_client.domain import APIConfig


class DataMasterApi(metaclass=abc.ABCMeta):
    """
    Базовый класс для методов API дата мастера
    """
    class Error(Exception):
        """ """

    class MisconfiguredError(Error):
        """ Ошибка """

    def __init__(self, api_config: APIConfig):
        self.api_config = api_config

    @abc.abstractmethod
    def load_model(self, model_id: int, **options) -> pandas.DataFrame:
        """ """

    @abc.abstractmethod
    def model_schema(self, model_id: int) -> ModelSchema:
        """ """

    @abc.abstractmethod
    def load_model_object_data(self, folder: Path, model_id: int, model_object_name: str, limit: Optional[int]):
        """ """

    @contextmanager
    def get_http_client(self) -> httpx.Client:
        """ """
        if not self.api_config.aw_url:
            raise DataMasterApi.MisconfiguredError('Не указан URL к Analytic Workspace')

        if not self.api_config.token:
            raise DataMasterApi.MisconfiguredError('Не указано токен доступа к Analytic Workspace')

        headers = {"Authorization": f"Bearer {self.api_config.token}"}

        client = httpx.Client(base_url=self.api_config.aw_url, headers=headers)

        try:
            yield client
        finally:
            client.close()
