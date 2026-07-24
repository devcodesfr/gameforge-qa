from __future__ import annotations

import uuid

import pytest

from qa_client.config import QaConfig
from qa_client.gfs_client import GfsClient


def test_authenticated_community_post_round_trip(qa_config: QaConfig) -> None:
    accounts = qa_config.cross_app_accounts
    if not accounts:
        pytest.skip("Set GFS role test credentials to run community persistence QA.")

    account = accounts[0]
    client = GfsClient(qa_config.gfs_api_url)
    login = client.login(account.username or "", account.password or "")
    assert login.status_code == 200, login.text

    content = f"QA persistence check {uuid.uuid4()}"
    created = client.create_community_post(content)
    assert created.status_code == 201, created.text
    created_post = created.json()
    assert created_post["content"] == content

    fetched = client.community_posts()
    assert fetched.status_code == 200, fetched.text
    assert any(
        post["id"] == created_post["id"] and post["content"] == content
        for post in fetched.json()
    )
