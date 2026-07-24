from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import pytest

from qa_client.config import QaConfig
from qa_client.gfs_client import GfsClient
from qa_client.buttonz_client import ButtonzClient


def extract_code(launch_url: str) -> str:
    parsed = urlparse(launch_url)
    values = parse_qs(parsed.query).get("code", [])
    assert values, f"Expected launch URL to include code query param: {launch_url}"
    return values[0]


def test_gfs_to_buttonz_auth_handoff(qa_config: QaConfig) -> None:
    if not qa_config.cross_app_accounts:
        pytest.skip("Set GFS role test credentials in .env to run cross-app auth QA.")

    for account in qa_config.cross_app_accounts:
        gfs_client = GfsClient(qa_config.gfs_api_url)
        buttonz_client = ButtonzClient(qa_config.buttonz_api_url)

        login = gfs_client.login(account.username or "", account.password or "")
        assert login.status_code == 200, f"{account.label}: {login.text}"
        gfs_user = login.json()["user"]

        launch = gfs_client.create_buttonz_launch()
        assert launch.status_code == 200, f"{account.label}: {launch.text}"

        launch_url = launch.json()["launchUrl"]
        code = extract_code(launch_url)

        exchange = buttonz_client.exchange_gfs_code(code)
        assert exchange.status_code == 200, f"{account.label}: {exchange.text}"

        current = buttonz_client.current_user()
        assert current.status_code == 200, f"{account.label}: {current.text}"
        assert current.json()["id"] == gfs_user["id"]

        # A second request proves Buttonz retained its own session after exchange.
        repeated_current = buttonz_client.current_user()
        assert repeated_current.status_code == 200, (
            f"{account.label}: {repeated_current.text}"
        )
        assert repeated_current.json()["id"] == gfs_user["id"]

        # Authorization codes are one-time use, even from a fresh Buttonz session.
        replay = ButtonzClient(qa_config.buttonz_api_url).exchange_gfs_code(code)
        assert replay.status_code == 401, f"{account.label}: {replay.text}"
