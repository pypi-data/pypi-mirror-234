"""
file locator
"""
import os
from lottostar_cli.app.config.main import settings


class FileLocator:
    """
    file locator
    """
    def __init__(self, file_name: str = "") -> None:
        """
        init method
        """
        self.file_name = file_name
        self.home_dir = os.path.dirname(os.getcwd()) if \
            int(os.getenv('CELERY_CONTAINER', '0')) == 1 else os.getcwd()
        self.file_path = os.path.join(
            self.home_dir,
            settings.DEFAULT_SFTP_FOLDER,
            self.file_name
        )

    def _validate_winning_entry_file(self) -> bool:
        """
        Encapsulate the validation of the winning entry file.
        Winning entry files must have the word
        'result' in the filename.
        """
        try:
            file_name_array = self.file_name.split(" ")
            file_is_winning_entry_file = \
                settings.WINNING_ENTRY_FILE_IDENTIFIER in \
                file_name_array[1]
        except IndexError:
            file_is_winning_entry_file = False

        return os.path.exists(self.file_path) and file_is_winning_entry_file

    def get_results_file_path(self) -> str:
        """
        Get results file path.
        First check if the file is valid.
        """
        if not self._validate_winning_entry_file():
            raise FileNotFoundError(
                f"Unable to process file {self.file_name} at: {self.file_path}"
            )

        return self.file_path

    def get_output_file_path(self) -> str:
        """
        Get output file path.
        No need to validate the file here.
        Process will fail at get_results_file_path if the file is invalid.
        """
        output_file_name = f"{self.file_name.split('.')[0]}-output.csv"
        return os.path.join(
            self.home_dir,
            settings.DEFAULT_OUTPUT_FOLDER,
            output_file_name
        )

    def get_entry_tickets_file_path(self) -> str:
        """
        Get entry tickets file path.
        No need to validate the file here.
        """
        file_path_without_extension = self.file_path.split('.')[0]
        entry_tickets_file_path = \
            file_path_without_extension.split(' ')[0]

        if not os.path.exists(f"{entry_tickets_file_path}.csv"):
            raise FileNotFoundError(
                f"Unable to process file {self.file_name} at: {self.file_path}"
            )

        return f"{entry_tickets_file_path}.csv"
