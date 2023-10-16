"""
Settings for the app
"""
import os
from dataclasses import dataclass


# pylint: disable=invalid-name
@dataclass
class Settings:
    """
    settings data class
    """
    DEFAULT_SFTP_FOLDER: str = "SFTP/inputs"
    DEFAULT_OUTPUT_FOLDER: str = "SFTP/outputs"
    WINNING_ENTRY_FILE_IDENTIFIER: str = "result"
    WINNING_ENTRY_DATA_ROW: str = 4
    #  pylint: disable=invalid-name
    CELERY_BROKER_URL: str = os.getenv(
        'REDIS_HOST',
        'redis://localhost:6379/0'
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        'REDIS_HOST',
        'redis://localhost:6379/0'
    )
    DEFAULT_CELERY_APP_NAME: str = 'lottostar_celery'
    CELERY_IMPORTS = ["app.cli.main"]


settings = Settings()
