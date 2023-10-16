from hashlib import md5
from urllib.parse import urlparse
from pathlib import Path

from aw_client.models.model_schema import ModelSchema, ModelObject


class ModelDevCache:
    """ """
    def __init__(self, cache_root_folder: Path, aw_url: str, model_id: int, is_full: bool = False):
        """ """
        self.cache_root_folder = cache_root_folder
        self.aw_url = aw_url
        self.model_id = model_id
        self.is_full = is_full

        self.aw_netloc = urlparse(aw_url).netloc.replace(":", "_")

    def get_model_folder(self) -> Path:
        """ """
        return Path(self.cache_root_folder) / self.aw_netloc / f'model_{self.model_id}'

    def model_schema_path(self) -> Path:
        return self.get_model_folder() / 'model_schema.json'

    def model_source_folder(self) -> Path:
        """ """
        return self.get_model_folder() / ('full' if self.is_full else 'part')

    def model_object_data_folder(self, model_object_name: str) -> Path:
        """ """
        return self.model_source_folder() / f'{model_object_name}.parquet'

    def model_object_hash_path(self, model_object: ModelObject) -> Path:
        """ """
        return self.model_source_folder() / f'{model_object.model_name}.hash'

    def set_model_object_hash(self, model_object: ModelObject):
        """ """
        with open(self.model_object_hash_path(model_object), 'wt') as f:
            f.write(self._model_object_hash(model_object))

    def is_model_object_actual(self, model_object: ModelObject) -> bool:
        """ """
        try:
            model_object_hash_path = self.model_object_hash_path(model_object)
            if not model_object_hash_path.exists():
                return False

            with open(self.model_object_hash_path(model_object), 'rt') as f:
                return f.read() == self._model_object_hash(model_object)
        except:
            return False

    @staticmethod
    def _model_object_hash(model_object: ModelObject) -> str:
        return md5(model_object.json(ensure_ascii=False, sort_keys=True).encode()).hexdigest()
