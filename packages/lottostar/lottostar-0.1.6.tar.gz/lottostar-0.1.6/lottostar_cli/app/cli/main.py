"""
cli module
"""
import os
import click
from celery import shared_task
from lottostar_cli.app.celery.celery_launcher import celery_app
from lottostar_cli.app.file_processor.file_locator import FileLocator
from lottostar_cli.app.file_processor.csv_processor import \
    WinningEntryCsvProcessor, OutputCsvProcessor
from lottostar_cli.app.ballsets.main import BallSet
from lottostar_cli.app.tickets.main import Ticket


@click.group()
def cli():
    """
    cli group
    """
    pass  # pylint: disable=unnecessary-pass


@shared_task()
def processor(filename: str) -> None:
    """
    Process lottery results
    """
    file_locator = FileLocator(filename)
    winning_entry_numbers = WinningEntryCsvProcessor(file_locator)\
        .process()
    ballset = BallSet(winning_entry_numbers)
    winning_ticket = Ticket(ballset)
    OutputCsvProcessor(file_locator, winning_ticket).process()


@click.command()
@click.option("-f", "--filename",
              prompt="Please enter the lottery results filename",
              required=True)
def process_lottery_results_sync(filename: str) -> None:
    """
    Process an independent national lottery results.
    """
    processor(filename)


@click.command()
def process_all_lottery_results_async() -> None:
    """
    process all 30 independent national lottery results.
    """
    # get all files in the sftp folder
    file_locator = FileLocator()
    sftp_folder_files = os.listdir(file_locator.file_path)
    result_files = [file for file in sftp_folder_files if 'result' in file]
    try:
        # run each file process using celery worker
        for result_file in result_files:
            celery_app.send_task(
                'app.cli.main.processor',
                args=[result_file]
            )
    except Exception as error:
        # raise exception celery worker fails
        raise error


cli.add_command(process_lottery_results_sync, "process")  # command name
cli.add_command(process_all_lottery_results_async,
                "parallel-process")  # command name
