import pytest
import os
import pathlib


@pytest.fixture(scope="session")
def tmp_datasets_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


_THIS_FILE = pathlib.Path(__file__).parent.absolute()


def get_data_path(subpath: str = ""):
    return os.path.join(_THIS_FILE, "data" + os.sep, subpath)


def data_path(file_name: str = ""):
    path = get_data_path()
    return os.path.join(path, file_name)
