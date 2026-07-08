from __future__ import annotations

from qa_client.buttonz_client import ButtonzClient
from qa_client.config import QaConfig
from qa_client.gfs_client import GfsClient


def test_gfs_health(gfs_client: GfsClient) -> None:
    response = gfs_client.health()

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_buttonz_health(buttonz_client: ButtonzClient) -> None:
    response = buttonz_client.health()

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_gfs_current_user_logged_out(gfs_client: GfsClient) -> None:
    response = gfs_client.current_user()

    assert response.status_code == 401


def test_buttonz_current_user_logged_out(buttonz_client: ButtonzClient) -> None:
    response = buttonz_client.current_user()

    assert response.status_code == 401


def test_buttonz_config_exposes_gfs_public_url(
    buttonz_client: ButtonzClient,
    qa_config: QaConfig,
) -> None:
    response = buttonz_client.config()

    assert response.status_code == 200
    assert response.json()["gameforgePublicUrl"].rstrip("/") == qa_config.gfs_public_url
