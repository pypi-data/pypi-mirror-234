"""
ballset module
"""


# pylint: disable=too-few-public-methods
class BallSet:
    """
    Ballset class.
    Sets the ballset for a lottery
    and additional ballsets
    """

    def __init__(self, entry_numbers: str):
        self.main_ballset = []
        self.additional_ballsets = []
        self.entry_numbers = entry_numbers
        self._describe_ballset()

    def _describe_ballset(self) -> None:
        """
        Extract ballset and additional ballsets from entry_numbers
        """
        groups = self.entry_numbers.split(';')
        self.main_ballset = [int(ball) for ball in groups[0].split(':')]
        if len(groups) > 1:
            array_excluding_main_ball_set = groups[1:]
            # set additional ballsets to list excluding empty strings
            self.additional_ballsets = [
                int(value) for value in
                array_excluding_main_ball_set if value != ""
            ]
