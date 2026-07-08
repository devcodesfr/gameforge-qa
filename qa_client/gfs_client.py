from __future__ import annotations

import requests


class GfsClient:
    def __init__(self, base_url: str, session: requests.Session | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def health(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/health")

    def current_user(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/user/current")

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/auth/login",
            json={"username": username, "password": password},
        )

    def create_buttonz_launch(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/api/external-apps/buttonz/launch")
