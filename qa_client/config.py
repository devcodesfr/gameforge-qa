import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class TestAccount:
    label: str
    username: str | None
    password: str | None

    @property
    def has_credentials(self) -> bool:
        return bool(
            self.username
            and self.password
            and not self.username.startswith("your-")
            and not self.password.startswith("your-")
        )


@dataclass(frozen=True)
class QaConfig:
    gfs_api_url: str
    gfs_public_url: str
    buttonz_api_url: str
    gfs_admin_username: str | None
    gfs_admin_password: str | None
    gfs_developer_username: str | None
    gfs_developer_password: str | None
    gfs_gamer_username: str | None
    gfs_gamer_password: str | None

    @property
    def cross_app_accounts(self) -> list[TestAccount]:
        accounts = [
            TestAccount("developer", self.gfs_developer_username, self.gfs_developer_password),
            TestAccount("gamer", self.gfs_gamer_username, self.gfs_gamer_password),
        ]
        return [account for account in accounts if account.has_credentials]


def load_config() -> QaConfig:
    return QaConfig(
        gfs_api_url=os.getenv("GFS_API_URL", "http://127.0.0.1:5000").rstrip("/"),
        gfs_public_url=os.getenv("GFS_PUBLIC_URL", "http://localhost:5173").rstrip("/"),
        buttonz_api_url=os.getenv("BUTTONZ_API_URL", "http://127.0.0.1:5001").rstrip("/"),
        gfs_admin_username=os.getenv("GFS_ADMIN_USERNAME"),
        gfs_admin_password=os.getenv("GFS_ADMIN_PASSWORD"),
        gfs_developer_username=os.getenv("GFS_DEVELOPER_USERNAME"),
        gfs_developer_password=os.getenv("GFS_DEVELOPER_PASSWORD"),
        gfs_gamer_username=os.getenv("GFS_GAMER_USERNAME"),
        gfs_gamer_password=os.getenv("GFS_GAMER_PASSWORD"),
    )
