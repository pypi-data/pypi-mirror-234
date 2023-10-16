"""
CSV file processor. Reads CSV files and writes to CSV files.
"""
import csv
from abc import ABC, abstractmethod
from lottostar_cli.app.config.main import settings
from lottostar_cli.app.tickets.main import Ticket
from lottostar_cli.app.ballsets.main import BallSet
from .file_locator import FileLocator


# pylint: disable=too-few-public-methods
class AbstractCsvProcessor(ABC):
    """
    Abstract CSV processor
    """
    def __init__(self, file: FileLocator, ticket: Ticket = None) -> None:
        self.file = file
        self.ticket = ticket

    @abstractmethod
    def process(self):
        """
        Abstract process method
        """
        pass  # pylint: disable=unnecessary-pass


# pylint: disable=too-few-public-methods
class WinningEntryCsvProcessor(AbstractCsvProcessor):
    """
    Input CSV file processor
    """
    def process(self) -> str:
        """
        Process the CSV file
        """
        with open(self.file.get_results_file_path(),
                  "r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            # skip to where the winning entry numbers are
            data_row = next(
                row for row_index, row in enumerate(csv_reader, start=1) if
                row_index == settings.WINNING_ENTRY_DATA_ROW
            )
            return data_row[0]


class OutputCsvProcessor(AbstractCsvProcessor):
    """
    Process output csv file with:
    1. Count of matched numbers
    2. Count of matched numbers
    3. If a Ticket has matched all numbers,
    indicate that the jackpot was won
    """
    # pylint: disable=fixme
    # TODO: refactoring needed here
    def process(self) -> None:
        """
        Process the CSV file
        """
        winning_ticket = self.ticket
        print(f"🏆🏆🏆 Winning ticket main balleset: "
              f"{winning_ticket.ballset.main_ballset} Additional "
              f"ballsets: {winning_ticket.ballset.additional_ballsets} "
              f"🏆🏆🏆\n\n")

        with open(self.file.get_entry_tickets_file_path(),
                  mode='r', newline='', encoding="utf-8") as input_file:
            # read the input file (entry tickets)
            csv_reader = csv.reader(input_file)
            # skip header
            next(csv_reader)

            # write to the output file
            with open(self.file.get_output_file_path(),
                      mode='w', newline='', encoding="utf-8") as output_file:
                csv_writer = csv.writer(output_file)
                # write header
                csv_writer.writerow([
                    "ticket_number",
                    "main_ballset_matches",
                    "additional_ballsets_matches",
                    "jackpot_won"
                ])
                for row in csv_reader:
                    # process entry ticket
                    if len(row) == 0:
                        continue

                    # get entry ticket array
                    # [ticket_number, ballset_1, ballset_2, ballset_3 etc...]
                    entry_ticket_array = row[0].split(";")
                    # pass ballset to ticket excluding ticket number
                    ticket_ballset = BallSet(";".join(entry_ticket_array[1:]))
                    ticket = Ticket(
                        ballset=ticket_ballset,
                        ticket_number=entry_ticket_array[0]
                    )

                    print(f"Processing entry ticket: {ticket.ticket_number}."
                          f" Main balleset:"
                          f" {ticket.ballset.main_ballset}"
                          f"Additional ballsets:"
                          f" {ticket.ballset.additional_ballsets}")

                    # get matched numbers from the main ballset
                    winning_set = set(winning_ticket.ballset.main_ballset)
                    ticket_set = set(ticket.ballset.main_ballset)
                    matched_numbers = list(
                        winning_set.intersection(ticket_set)
                    )

                    # get matched numbers from the additional ballsets
                    winning_additional_sets = set(
                        winning_ticket.ballset.additional_ballsets
                    )
                    ticket_additional_sets = set(
                        ticket.ballset.additional_ballsets
                    )
                    matched_additional_numbers = list(
                        winning_additional_sets
                        .intersection(ticket_additional_sets)
                    )

                    # write to output file
                    jackpot_won = len(matched_numbers) + \
                        len(matched_additional_numbers) \
                        == len(winning_ticket.ballset.main_ballset) + \
                        len(winning_ticket.ballset.additional_ballsets)

                    csv_writer.writerow([
                        ticket.ticket_number,
                        len(matched_numbers),
                        len(matched_additional_numbers),
                        jackpot_won
                    ])

                print("\n\n🏆🏆🏆 Processing complete 🏆🏆🏆")
