from __future__ import annotations

import pytest

from qa_client.config import QaConfig, TestAccount as QaTestAccount
from qa_client.gfs_client import GfsClient


def admin_account(qa_config: QaConfig) -> QaTestAccount:
    return QaTestAccount(
        "admin",
        qa_config.gfs_admin_username,
        qa_config.gfs_admin_password,
    )


def developer_account(qa_config: QaConfig) -> QaTestAccount:
    return QaTestAccount(
        "developer",
        qa_config.gfs_developer_username,
        qa_config.gfs_developer_password,
    )


def gamer_account(qa_config: QaConfig) -> QaTestAccount:
    return QaTestAccount(
        "gamer",
        qa_config.gfs_gamer_username,
        qa_config.gfs_gamer_password,
    )


def test_admin_can_view_system_health(qa_config: QaConfig) -> None:
    account = admin_account(qa_config)
    if not account.has_credentials:
        pytest.skip("Set GFS Admin Developer test credentials to run system health QA.")

    client = GfsClient(qa_config.gfs_api_url)
    login = client.login(account.username or "", account.password or "")
    assert login.status_code == 200, login.text

    current_user = client.current_user()
    assert current_user.status_code == 200, current_user.text
    user = current_user.json()
    assert user["role"] == "developer"
    assert user["isAdmin"] is True

    response = client.system_health()
    assert response.status_code == 200, response.text

    payload = response.json()
    components = {component["id"]: component for component in payload["components"]}

    assert payload["status"] == "operational"
    assert set(components) == {
        "gfs-api",
        "database",
        "buttonz-api",
        "authentication",
    }
    assert components["gfs-api"]["status"] == "operational"
    assert components["database"]["status"] == "operational"
    assert components["buttonz-api"]["status"] == "operational"
    assert components["authentication"]["status"] == "operational"

    # CI telemetry is non-critical and may be disabled or rate-limited.
    assert payload["automation"]["status"] in {
        "available",
        "unavailable",
        "not_configured",
    }

    attempted_update = client.update_profile(user["id"], {"isAdmin": False})
    assert attempted_update.status_code == 400, attempted_update.text
    current_user_after_update = client.current_user()
    assert current_user_after_update.status_code == 200, current_user_after_update.text
    assert current_user_after_update.json()["isAdmin"] is True


def test_developer_cannot_view_system_health(
    qa_config: QaConfig,
) -> None:
    account = developer_account(qa_config)
    if not account.has_credentials:
        pytest.skip("Set GFS Developer test credentials to run system health QA.")

    client = GfsClient(qa_config.gfs_api_url)
    login = client.login(account.username or "", account.password or "")
    assert login.status_code == 200, login.text

    current_user = client.current_user()
    assert current_user.status_code == 200, current_user.text
    assert current_user.json()["isAdmin"] is False

    response = client.system_health()
    assert response.status_code == 403


def test_gamer_cannot_view_system_health(qa_config: QaConfig) -> None:
    account = gamer_account(qa_config)
    if not account.has_credentials:
        pytest.skip("Set GFS Gamer test credentials to run system health QA.")

    client = GfsClient(qa_config.gfs_api_url)
    login = client.login(account.username or "", account.password or "")
    assert login.status_code == 200, login.text

    response = client.system_health()
    assert response.status_code == 403
