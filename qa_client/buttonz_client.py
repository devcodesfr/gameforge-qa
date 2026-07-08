from __future__ import annotations

import requests


class ButtonzClient:
    def __init__(self, base_url: str, session: requests.Session | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()

    def health(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/health")

    def config(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/config")

    def current_user(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/user/current")

    def exchange_gfs_code(self, code: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/auth/gfs-session",
            json={"code": code},
        )
