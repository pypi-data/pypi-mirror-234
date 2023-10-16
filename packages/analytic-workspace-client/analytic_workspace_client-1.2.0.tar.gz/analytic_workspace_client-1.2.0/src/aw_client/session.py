from typing import Optional

import os
from pathlib import Path

import httpx
import pandas
from contextlib import contextmanager
from urllib.parse import urljoin

from aw_client.data_master import get_nearest_api
from aw_client.domain import APIConfig
from aw_client.models.model_schema import ModelSchema
from aw_client.exceptions import AwClientMisconfigured

from aw_client.tools import strip_column_name_prefix


class Session:
    """
    Сессия подключения к AW
    """
    class Error(Exception):
        """ """

    def __init__(self, token: str = None, aw_url: str = None, version: int = None):
        """ """
        self.token = (token or os.getenv("AW_DATA_TOKEN") or '').strip()
        self.aw_url = (aw_url or os.getenv('AW_URL') or '').strip()
        if not self.aw_url:
            raise AwClientMisconfigured(
                'Укажите URL к AnalyticWorkspace: Session(aw_url=\'http://aw.mydomain.ru\') или установите переменную '
                'окружения AW_URL')
        if not self.aw_url.endswith('/'):
            self.aw_url += '/'
        self.version = version if version is not None else None

    def get_aw_version(self) -> int:
        """ """
        if self.version is None:
            with self.get_aw_client() as client:
                r = client.get('data-master/_version')
                if r.is_success:
                    self.version = r.json().get('version')
                elif r.status_code == 404:
                    self.version = 0  # для версии 0 как раз нет
                else:
                    raise Session.Error(f'Ошибка HTTP {r.status_code} запроса GET {r.url}: {r.text}')
        if self.version is None:
            raise Session.Error('Не удалось определить версию AW')

        return self.version

    def load_model(self, model_id: int, strip_prefix: bool = False, **options) -> pandas.DataFrame:
        """
        Загружает данные модели в датафрейм pandas
        """
        if not self.aw_url:
            raise Session.Error('Не указан URL к Analytic Workspace (параметр aw_url)')

        if not self.token:
            raise Session.Error('Не указан токен доступа к Analytic Workspace (параметр token)')

        api_config = APIConfig(
            aw_url=self.aw_url,
            token=self.token
        )

        api, version = get_nearest_api(aw_version=self.get_aw_version(), api_config=api_config)
        if api is None:
            raise Session.Error(f'Не удалось получить API для версии AW {self.version}')

        df = api.load_model(model_id=model_id, **options)
        if strip_prefix:
            df = strip_column_name_prefix(df, inplace=True)

        return df

    def model_schema(self, model_id: int) -> ModelSchema:
        """ """
        if not self.aw_url:
            raise Session.Error('Не указан URL к Analytic Workspace (параметр aw_url)')

        if not self.token:
            raise Session.Error('Не указан токен доступа к Analytic Workspace (параметр token)')

        api_config = APIConfig(
            aw_url=self.aw_url,
            token=self.token
        )

        api, version = get_nearest_api(aw_version=self.get_aw_version(), api_config=api_config)
        if api is None:
            raise Session.Error(f'Не удалось получить API для версии AW {self.version}')

        return api.model_schema(model_id)

    def load_model_object_data(self, folder: Path, model_id: int, model_object_name: str, limit: Optional[int]):
        """ """
        if not self.aw_url:
            raise Session.Error('Не указан URL к Analytic Workspace (параметр aw_url)')

        if not self.token:
            raise Session.Error('Не указан токен доступа к Analytic Workspace (параметр token)')

        api_config = APIConfig(
            aw_url=self.aw_url,
            token=self.token
        )

        api, version = get_nearest_api(aw_version=self.get_aw_version(), api_config=api_config)
        if api is None:
            raise Session.Error(f'Не удалось получить API для версии AW {self.version}')

        return api.load_model_object_data(folder, model_id, model_object_name, limit)

    @contextmanager
    def get_aw_client(self) -> httpx.Client:
        """ """
        if not self.aw_url:
            raise Session.Error('Не указан URL к Analytic Workspace')

        headers = {"Authorization": f"Bearer {self.token}"}

        client = httpx.Client(base_url=self.aw_url, headers=headers)

        try:
            yield client
        finally:
            client.close()

    @property
    def mlflow(self):
        """ """
        try:
            import mlflow
        except ImportError:
            raise AwClientMisconfigured(
                'Для использованиея MLFlow установите с зависимостью ml: pip install aw_client[ml]')

        if not self.token:
            data_master_url = urljoin(self.aw_url, 'data-master/get-token')
            raise AwClientMisconfigured(
                f'Не указан токен доступа к AnalyticWorkspace. Пройдите по адресу {data_master_url} для получения '
                f'токена')

        tracking_url = urljoin(self.aw_url, 'mlflow')

        if mlflow.get_tracking_uri() != tracking_url:
            mlflow.set_tracking_uri(tracking_url)

        os.environ['MLFLOW_TRACKING_TOKEN'] = self.token

        return mlflow
