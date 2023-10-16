import os
import logging
import logging.config
from typing import Optional
from pydantic import BaseSettings, PostgresDsn, validator
from pathlib import Path

DEFAULT_DATA_DIR = Path.home() / ".shipyard"
DEFAULT_SQLITE_FILENAME = Path("shipyard.db")


def logging_config(data_dir: Path):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(name)s (%(levelname)s): %(message)s"},
            "logfile": {
                "format": "%(asctime)s %(name)s (%(levelname)s): %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "rotating_file": {
                "level": "DEBUG",
                "formatter": "logfile",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": data_dir / "shipyard.log",
                "when": "W6",
            },
        },
        "loggers": {
            "shipyard": {
                "handlers": ["default", "rotating_file"],
                "level": "DEBUG",
                "propagate": True,
            }
        },
    }


class Settings(BaseSettings):
    data_dir: Path = DEFAULT_DATA_DIR
    sqlite_filename: Path = DEFAULT_SQLITE_FILENAME
    postgres_url: Optional[PostgresDsn] = None

    @validator("data_dir")
    def expand_data_dir(cls, val):
        return Path(val).expanduser()

    class Config:
        env_prefix = "shipyard_"
        env_file = ".env"

    def ensure_data_dir(self):
        data_dir = self.data_dir

        if data_dir.is_file():
            raise FileExistsError(f"{data_dir} is a regular file.")

        if data_dir.is_symlink() and not data_dir.exists():
            raise FileExistsError(f"{data_dir} is a broken link.")

        if not data_dir.is_dir():
            print(f"Creating data directory {data_dir}{os.sep}")
            data_dir.mkdir()

        logging.config.dictConfig(logging_config(self.data_dir))


class SettingsException(Exception):
    pass


_settings: Optional[Settings] = None


def load_settings(**kwargs) -> Settings:
    global _settings
    if _settings:
        raise SettingsException("Settings must be loaded only once.")
    else:
        _settings = Settings(**kwargs)
    return _settings


def get_settings() -> Settings:
    global _settings
    if not _settings:
        raise SettingsException("Settings must be loaded before being used.")
    return _settings
