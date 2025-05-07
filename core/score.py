import pandas as pd
from typing import Union


class GameScoreManager:
    """
    Manages game scores, stores them in a CSV file, and provides methods to interact with the data.
    """
    def __init__(self):
        """
        Initialize the GameScoreManager instance.

        The data is loaded from an existing CSV file or an empty DataFrame is created if the file doesn't exist.
        """
        self.file_path = "data/score.csv"
        self.load_data()

    def load_data(self) -> None:
        """
        Load game score data from a CSV file.

        If the file doesn't exist, an empty DataFrame is created.

        :return: None
        """
        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            # Create an empty DataFrame if the file doesn't exist
            self.data = pd.DataFrame(columns=['CPS', 'Time', 'Mode'])

    def save_data(self) -> None:
        """
        Save the current game score data to a CSV file.

        :return: None
        """
        self.data.to_csv(self.file_path, index=False)

    def add_score(self, cps: float, time: int, click: bool, buy_out: bool, ratio: Union[str, None] = None) -> None:
        """
        Add a new game score to the data.

        Used by the CookieClickerBot instance at the end of the game.

        :param cps: Cookies per second value.
        :type cps: float
        :param time: Time in seconds.
        :type time: int
        :param click: Game mode (e.g., "manual" or "automated").
        :type click: bool
        :param buy_out: Game mode (e.g., "manual" or "automated").
        :type buy_out: bool
        :param ratio: Game mode (e.g., "manual" or "automated").
        :type ratio: str, None
        :return: None
        """
        if click and buy_out:
            mode = f"Full-Auto[{ratio}]"
        elif click and not buy_out:
            mode = "Clicker"
        elif not click and buy_out:
            mode = f"Buy-Out[{ratio}]"
        else:
            mode = "Manual"

        new_row = {'CPS': cps, 'Time': time, 'Mode': mode}
        self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data()

    def get_leaderboard(self) -> pd.DataFrame:
        """
        Retrieve the leaderboard sorted by Cookies per Second (CPS) in descending order.

        :return: Leaderboard DataFrame.
        :rtype: pd.DataFrame
        """
        leaderboard = self.data.sort_values(by='CPS', ascending=False)
        return leaderboard

