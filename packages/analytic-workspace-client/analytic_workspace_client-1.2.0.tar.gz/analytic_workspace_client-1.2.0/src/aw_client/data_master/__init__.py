from typing import Tuple, Optional, Callable

from importlib import import_module

from .base import DataMasterApi
from ..domain import APIConfig


def get_nearest_api(aw_version: int, api_config: APIConfig, exact_version: bool = False) -> Tuple[Optional[DataMasterApi], Optional[int]]:
    """ """
    api_cls = None
    version = None

    # передираем все доступные APi
    for version in range(aw_version, (aw_version - 1) if exact_version else -1, -1):
        module_name = f'aw_client.data_master.v{version}'
        class_name = f'DataMasterV{version}'

        try:
            api_mdl = import_module(module_name)
            api_cls = getattr(api_mdl, class_name, None)
        except ImportError:
            continue

        if api_cls is not None:
            break

    return api_cls(api_config) if api_cls is not None else None, version
