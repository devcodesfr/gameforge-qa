from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest

from qa_client.buttonz_client import ButtonzClient
from qa_client.config import QaConfig
from qa_client.gfs_client import GfsClient


def extract_code(launch_url: str) -> str:
    parsed = urlparse(launch_url)
    values = parse_qs(parsed.query).get("code", [])
    assert values, f"Expected launch URL to include code query param: {launch_url}"
    return values[0]


def test_gfs_to_buttonz_auth_handoff(
    gfs_client: GfsClient,
    buttonz_client: ButtonzClient,
    qa_config: QaConfig,
) -> None:
    if not qa_config.has_gfs_credentials:
        pytest.skip("Set GFS_TEST_USERNAME and GFS_TEST_PASSWORD in .env to run cross-app auth QA.")

    login = gfs_client.login(
        qa_config.gfs_test_username or "",
        qa_config.gfs_test_password or "",
    )
    assert login.status_code == 200, login.text
    gfs_user = login.json()["user"]

    launch = gfs_client.create_buttonz_launch()
    assert launch.status_code == 200, launch.text

    launch_url = launch.json()["launchUrl"]
    code = extract_code(launch_url)

    exchange = buttonz_client.exchange_gfs_code(code)
    assert exchange.status_code == 200, exchange.text

    current = buttonz_client.current_user()
    assert current.status_code == 200, current.text
    assert current.json()["id"] == gfs_user["id"]
