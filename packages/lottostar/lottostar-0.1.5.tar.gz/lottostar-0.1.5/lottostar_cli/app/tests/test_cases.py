"""
Test cases
"""
import pytest
from lottostar_cli.app.file_processor.csv_processor import WinningEntryCsvProcessor, \
    OutputCsvProcessor
from lottostar_cli.app.file_processor.file_locator import FileLocator
from lottostar_cli.app.ballsets.main import BallSet
from lottostar_cli.app.tickets.main import Ticket


# test ballset construction
def test_ballset_construction():
    """
    test ballset construction
    """
    entry_numbers = [
        '1:12:5:23:42;7;',
        '2:13:12:21:20:4;7;',
        '1:2:5:24;4;1'
    ]

    entry_main_ballsets = [
        [1, 12, 5, 23, 42],
        [2, 13, 12, 21, 20, 4],
        [1, 2, 5, 24]
    ]

    entry_additional_ballsets = [
        [7],
        [7],
        [4, 1]
    ]

    ballsets = [
        BallSet(entry_number)
        for entry_number in entry_numbers
    ]

    assert [ballset.main_ballset for ballset in ballsets] == \
        entry_main_ballsets and \
        [ballset.additional_ballsets for ballset in ballsets] == \
        entry_additional_ballsets


# test CsvProcessor
def test_jackpot_won():
    """
    test jackpot won
    """
    file_locator = FileLocator(
        'jackpot_and_main_matches_test result.csv'
    )
    winning_entry_numbers = WinningEntryCsvProcessor(file_locator)\
        .process()
    ballset = BallSet(winning_entry_numbers)
    winning_ticket = Ticket(ballset)
    OutputCsvProcessor(file_locator, winning_ticket).process()

    with open(file_locator.get_output_file_path(), 'r',
              encoding="utf-8") as output_file:
        # check if jackpot has been won
        assert output_file.readlines()[1] == '1111131,5,1,True\n'


def test_winning_entry_csv_processor():
    """
    test winning entry csv processor
    """
    entry_numbers = [
        '1:12:5:23:42;7;',
        '2:13:12:21:20:4;7;',
        '1:2:5:24;4;1'
    ]

    entry_files = [
        'germany_03-11-2019_32322 result.csv',
        'italy_03-11-2019_32322 result.csv',
        'norway_06-11-2019_87685 result.csv'
    ]

    winning_entry_processes = [
        WinningEntryCsvProcessor(FileLocator(entry_file)).process()
        for entry_file in entry_files
    ]

    assert winning_entry_processes == entry_numbers


# test file locator
def test_input_file_validator():
    """
    test input file validator
    """
    with pytest.raises(FileNotFoundError) as error:
        file_locator = FileLocator('input.csv')
        file_locator.get_results_file_path()

    file_not_found_error = \
        'Unable to process file input.csv at: /SFTP/inputs/input.csv'
    assert str(error.value) == file_not_found_error


def test_input_file_locator():
    """
    test input file locator
    """
    file_locator = FileLocator('input.csv')
    assert file_locator.file_path == '/SFTP/inputs/input.csv'


def test_results_file_locator():
    """
    test results file locator
    """
    file_locator = FileLocator('input.csv')
    assert file_locator.get_output_file_path() ==\
        '/SFTP/outputs/input-output.csv'
