import os
import pytest
from uuid import uuid4
import posixpath
import deeplake

from deeplake.client.client import DeepLakeBackendClient
from deeplake.client.config import (
    USE_LOCAL_HOST,
    USE_DEV_ENVIRONMENT,
    USE_STAGING_ENVIRONMENT,
)

from .constants import *


from deeplake.core.storage.local import LocalProvider


SESSION_ID = "tmp" + str(uuid4())[:4]

@pytest.fixture
def local_path(request):

    path = posixpath.join(PYTEST_LOCAL_PROVIDER_BASE_ROOT, SESSION_ID)

    LocalProvider(path).clear()
    yield path

    LocalProvider(path).clear()

@pytest.fixture(scope="session")
def hub_cloud_dev_credentials(request):
    username = os.getenv(ENV_HUB_DEV_USERNAME)
    password = os.getenv(ENV_HUB_DEV_PASSWORD)

    assert (
        username is not None
    ), f"Deep Lake dev username was not found in the environment variable '{ENV_HUB_DEV_USERNAME}'. This is necessary for testing deeplake cloud datasets."
    assert (
        password is not None
    ), f"Deep Lake dev password was not found in the environment variable '{ENV_HUB_DEV_PASSWORD}'. This is necessary for testing deeplake cloud datasets."

    return username, password


@pytest.fixture(scope="session")
def hub_cloud_dev_token(hub_cloud_dev_credentials):
    username, password = hub_cloud_dev_credentials

    client = DeepLakeBackendClient()
    token = client.request_auth_token(username, password)
    return token

@pytest.fixture
def local_auth_ds_generator(local_path, hub_cloud_dev_token):
    def generate_local_auth_ds(**kwargs):
        return deeplake.dataset(local_path, token=hub_cloud_dev_token, **kwargs)

    return generate_local_auth_ds

@pytest.fixture
def local_auth_ds(local_auth_ds_generator):
    return local_auth_ds_generator()


@pytest.fixture
def local_ds_generator(local_path):
    def generate_local_ds(**kwargs):
        return deeplake.dataset(local_path, **kwargs)

    return generate_local_ds
