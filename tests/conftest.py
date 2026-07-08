from __future__ import annotations

import pytest

from qa_client.buttonz_client import ButtonzClient
from qa_client.config import QaConfig, load_config
from qa_client.gfs_client import GfsClient


@pytest.fixture(scope="session")
def qa_config() -> QaConfig:
    return load_config()


@pytest.fixture()
def gfs_client(qa_config: QaConfig) -> GfsClient:
    return GfsClient(qa_config.gfs_api_url)


@pytest.fixture()
def buttonz_client(qa_config: QaConfig) -> ButtonzClient:
    return ButtonzClient(qa_config.buttonz_api_url)
