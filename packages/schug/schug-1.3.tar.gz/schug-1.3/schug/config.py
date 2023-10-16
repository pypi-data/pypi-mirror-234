from pathlib import Path

from pydantic import BaseSettings

DEMO_DB: str = "sqlite://"
SCHUG_PACKAGE = Path(__file__).parent
PACKAGE_ROOT: Path = SCHUG_PACKAGE.parent
ENV_FILE: Path = PACKAGE_ROOT / ".env"


class Settings(BaseSettings):
    """Settings for serving the schug app"""

    db_uri: str = DEMO_DB
    host: str = "localhost"
    port: int = 8000

    class Config:
        from_file = str(ENV_FILE)


settings = Settings()
