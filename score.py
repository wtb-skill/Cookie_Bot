import pandas as pd


class GameScoreManager:
    """
    Manages game scores, stores them in a CSV file, and provides methods to interact with the data.
    """
    def __init__(self):
        """
        Initialize the GameScoreManager instance.

        The data is loaded from an existing CSV file or an empty DataFrame is created if the file doesn't exist.
        """
        self.file_path = "score.csv"
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

    def add_score(self, cps: float, time: int, mode: str = None) -> None:
        """
        Add a new game score to the data.

        :param cps: Cookies per second value.
        :type cps: float
        :param time: Time in seconds.
        :type time: int
        :param mode: Game mode (e.g., "manual" or "automated").
        :type mode: str, optional
        :return: None
        """
        if mode is None:
            mode = "manual"

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





