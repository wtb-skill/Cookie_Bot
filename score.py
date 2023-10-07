import pandas as pd


class GameScoreManager:
    def __init__(self):
        self.file_path = "score.csv"
        self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)
        except FileNotFoundError:
            # Create an empty DataFrame if the file doesn't exist
            self.data = pd.DataFrame(columns=['CPS', 'Time', 'Mode'])

    def save_data(self):
        self.data.to_csv(self.file_path, index=False)

    def add_score(self, cps, time, mode):
        if mode is None:
            mode = "manual"
        else:
            mode = mode
        new_row = {'CPS': cps, 'Time': time, 'Mode': mode}
        self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
        self.save_data()

    def get_leaderboard(self):
        leaderboard = self.data.sort_values(by='CPS', ascending=False)
        return leaderboard


# Example usage:
if __name__ == "__main__":
    score_manager = GameScoreManager()

    # Add new scores
    # score_manager.add_score(55, 100, 'no ratio')
    # score_manager.add_score(99, 60, 0.635)
    # score_manager.add_score(14, 60, 0.5)

    # Retrieve and display the leaderboard
    leaderboard = score_manager.get_leaderboard()
    print(leaderboard)



