import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class QaConfig:
    gfs_api_url: str
    gfs_public_url: str
    buttonz_api_url: str
    gfs_test_username: str | None
    gfs_test_password: str | None

    @property
    def has_gfs_credentials(self) -> bool:
        return bool(
            self.gfs_test_username
            and self.gfs_test_password
            and self.gfs_test_username != "your-test-user"
            and self.gfs_test_password != "your-test-password"
        )


def load_config() -> QaConfig:
    return QaConfig(
        gfs_api_url=os.getenv("GFS_API_URL", "http://127.0.0.1:5000").rstrip("/"),
        gfs_public_url=os.getenv("GFS_PUBLIC_URL", "http://localhost:5173").rstrip("/"),
        buttonz_api_url=os.getenv("BUTTONZ_API_URL", "http://127.0.0.1:5001").rstrip("/"),
        gfs_test_username=os.getenv("GFS_TEST_USERNAME"),
        gfs_test_password=os.getenv("GFS_TEST_PASSWORD"),
    )
