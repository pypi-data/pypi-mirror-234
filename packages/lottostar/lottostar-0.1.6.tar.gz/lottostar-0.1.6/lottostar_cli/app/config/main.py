"""
Settings for the app
"""
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


settings = Settings()
