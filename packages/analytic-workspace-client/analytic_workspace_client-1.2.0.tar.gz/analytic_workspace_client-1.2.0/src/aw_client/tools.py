import tempfile
import shutil
from pathlib import Path
from contextlib import contextmanager

import pandas as pd


@contextmanager
def get_temp_folder(remove_on_exit: bool = True) -> Path:
    """ """
    temp_folder = tempfile.mkdtemp()

    try:
        yield Path(temp_folder)
    finally:
        if remove_on_exit:
            shutil.rmtree(temp_folder, ignore_errors=True)


def strip_column_name_prefix(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
    """ 
    Вырезает общий префикс у столбцов датафрейма 
    """
    column_renames = {}
    for column_name in df.columns:
        if '__' in column_name:
            _, column_renames[column_name] = column_name.rsplit('__', 1)

    if column_renames:
        if inplace:
            df.rename(columns=column_renames, inplace=inplace)
        else:
            df.rename(columns=column_renames)

    return df
