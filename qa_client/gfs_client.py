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

    def system_health(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/system-health")

    def update_profile(self, user_id: str, updates: dict[str, object]) -> requests.Response:
        return self.session.patch(
            f"{self.base_url}/api/users/{user_id}",
            json=updates,
        )

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/auth/login",
            json={"username": username, "password": password},
        )

    def create_buttonz_launch(self) -> requests.Response:
        return self.session.post(f"{self.base_url}/api/external-apps/buttonz/launch")

    def community_posts(self) -> requests.Response:
        return self.session.get(f"{self.base_url}/api/community/posts")

    def create_community_post(self, content: str) -> requests.Response:
        return self.session.post(
            f"{self.base_url}/api/community/posts",
            json={"content": content, "type": "text"},
        )
