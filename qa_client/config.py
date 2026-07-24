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
            and self.username != "your-test-user"
            and self.password != "your-test-password"
        )


@dataclass(frozen=True)
class QaConfig:
    gfs_api_url: str
    gfs_public_url: str
    buttonz_api_url: str
    gfs_test_username: str | None
    gfs_test_password: str | None
    gfs_developer_username: str | None
    gfs_developer_password: str | None
    gfs_gamer_username: str | None
    gfs_gamer_password: str | None

    @property
    def has_gfs_credentials(self) -> bool:
        return bool(
            self.gfs_test_username
            and self.gfs_test_password
            and self.gfs_test_username != "your-test-user"
            and self.gfs_test_password != "your-test-password"
        )

    @property
    def cross_app_accounts(self) -> list[TestAccount]:
        accounts = [
            TestAccount("developer", self.gfs_developer_username, self.gfs_developer_password),
            TestAccount("gamer", self.gfs_gamer_username, self.gfs_gamer_password),
        ]

        configured_accounts = [account for account in accounts if account.has_credentials]
        if configured_accounts:
            return configured_accounts

        legacy_account = TestAccount("default", self.gfs_test_username, self.gfs_test_password)
        return [legacy_account] if legacy_account.has_credentials else []


def load_config() -> QaConfig:
    return QaConfig(
        gfs_api_url=os.getenv("GFS_API_URL", "http://127.0.0.1:5000").rstrip("/"),
        gfs_public_url=os.getenv("GFS_PUBLIC_URL", "http://localhost:5173").rstrip("/"),
        buttonz_api_url=os.getenv("BUTTONZ_API_URL", "http://127.0.0.1:5001").rstrip("/"),
        gfs_test_username=os.getenv("GFS_TEST_USERNAME"),
        gfs_test_password=os.getenv("GFS_TEST_PASSWORD"),
        gfs_developer_username=os.getenv("GFS_DEVELOPER_USERNAME"),
        gfs_developer_password=os.getenv("GFS_DEVELOPER_PASSWORD"),
        gfs_gamer_username=os.getenv("GFS_GAMER_USERNAME"),
        gfs_gamer_password=os.getenv("GFS_GAMER_PASSWORD"),
    )
