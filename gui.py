import tkinter as tk
from app_logic import play_game, show_leaderboard, show_help


class CookieClickerBotApp:
    """
    The main application for Cookie Clicker Bot.
    """
    BACKGROUND_COLOR_1 = "black"
    BACKGROUND_COLOR_2 = "peach puff"
    BACKGROUND_COLOR_3 = "lemon chiffon"
    BACKGROUND_COLOR_4 = "azure"

    def __init__(self, root: tk.Tk):
        """
        Initialize the CookieClickerBotApp instance.

        :param root: The main Tkinter root window.
        :type root: tk.Tk
        """
        self.root = root
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create and configure all the widgets for the application.

        :return: None
        """
        self.configure_root()
        self.load_cookie_image()
        self.create_play_button()
        self.create_bot_section()
        self.create_ratio_section()
        self.create_time_section()
        self.create_score_section()
        self.create_help_section()

    def configure_root(self) -> None:
        """
        Configure the main application window.

        :return: None
        """
        self.root.title("Cookie Clicker Bot")
        self.root.geometry("400x500")
        self.root.resizable(False, False)  # user unable to change the size of the window
        self.root.config(padx=10, pady=10, background=self.BACKGROUND_COLOR_1)

    def load_cookie_image(self) -> None:
        """
        Load the cookie image for the play button.

        :return: None
        """
        self.img = tk.PhotoImage(file='cookie.png')

    def create_play_button(self) -> None:
        """
        Create the play button widget.

        :return: None
        """
        self.button_play = tk.Button(
            self.root,
            text="Play",
            command=lambda: self.play_game(),
            height=350,
            width=260,
            image=self.img
        )
        self.button_play.grid(row=0, column=0, padx=10, pady=10, columnspan=5, sticky="NESW")

    def create_bot_section(self) -> None:
        """
        Create the section for bot options.

        :return: None
        """
        self.label_bot = tk.Label(self.root, text="Clicker", background=self.BACKGROUND_COLOR_2)
        self.label_bot.grid(row=1, column=0, padx=20)

        self.is_bot_on = tk.IntVar(value=1)
        self.radiobutton_bot_on = self.create_radiobutton(
            "On",
            1,
            self.is_bot_on,
            self.bot_options,
            self.BACKGROUND_COLOR_2,
            row=2,
            column=0
        )
        self.radiobutton_bot_off = self.create_radiobutton(
            "Off",
            2,
            self.is_bot_on,
            self.bot_options,
            self.BACKGROUND_COLOR_2,
            row=3,
            column=0
        )

    def create_ratio_section(self) -> None:
        """
        Create the section for ratio options.

        :return: None
        """
        self.label_ratio = tk.Label(self.root, text="Buy Out", background=self.BACKGROUND_COLOR_3)
        self.label_ratio.grid(row=1, column=1, padx=10)

        self.is_ratio_on = tk.IntVar(value=1)
        self.radiobutton_ratio_on = self.create_radiobutton(
            "On",
            1,
            self.is_ratio_on,
            self.ratio_options,
            self.BACKGROUND_COLOR_3,
            row=2,
            column=1
        )
        self.radiobutton_ratio_off = self.create_radiobutton(
            "Off",
            2,
            self.is_ratio_on,
            self.ratio_options,
            self.BACKGROUND_COLOR_3,
            row=3,
            column=1
        )

        self.entry_ratio = self.create_entry("0.625", row=2, column=2, background=self.BACKGROUND_COLOR_3)

    def create_time_section(self) -> None:
        """
        Create the section for time input.

        :return: None
        """
        self.label_time = tk.Label(self.root, text="Time", background=self.BACKGROUND_COLOR_4)
        self.label_time.grid(row=1, column=3, padx=20, pady=10)

        self.entry_time = self.create_entry("5", row=1, column=4, background=self.BACKGROUND_COLOR_4)

    def create_score_section(self) -> None:
        """
        Create the button to display the leaderboard.

        :return: None
        """
        self.button_score = tk.Button(
            self.root,
            text="Leaderboard",
            command=lambda: show_leaderboard(self.root),
        )
        self.button_score.grid(row=2, column=3)

    def create_help_section(self) -> None:
        """
        Create the button to display the help information.

        :return: None
        """
        self.button_help = tk.Button(
            self.root,
            text="Help",
            command=lambda: show_help(self.root),
        )
        self.button_help.grid(row=3, column=3)

# -----------------------------------------[Create from Tkinter objects]-----------------------------------------

    def create_radiobutton(self, text: str, value: int, variable: tk.IntVar, command, background: str,
                           row: int, column: int) -> tk.Radiobutton:
        """
        Create a radiobutton widget.

        :param text: Text label for the radiobutton.
        :type text: str
        :param value: Value associated with the radiobutton.
        :type value: int
        :param variable: IntVar to hold the selected value.
        :type variable: tk.IntVar
        :param command: Command to execute when the radiobutton is selected.
        :param background: Background color of the radiobutton.
        :type background: str
        :param row: Row position in the grid.
        :type row: int
        :param column: Column position in the grid.
        :type column: int
        :return: The created Radiobutton widget.
        :rtype: tk.Radiobutton
        """
        radiobutton = tk.Radiobutton(
            self.root,
            text=text,
            value=value,
            variable=variable,
            command=command,
            background=background,
        )
        radiobutton.grid(row=row, column=column)
        return radiobutton

    def create_entry(self, text: str, row: int, column: int, background: str) -> tk.Entry:
        """
        Create an entry widget.

        :param text: Default text for the entry.
        :type text: str
        :param row: Row position in the grid.
        :type row: int
        :param column: Column position in the grid.
        :type column: int
        :param background: Background color of the entry.
        :type background: str
        :return: The created Entry widget.
        :rtype: tk.Entry
        """
        entry = tk.Entry(
            self.root,
            width=5,
            background=background
        )
        entry.insert(tk.END, text)
        entry.grid(row=row, column=column, padx=20, pady=10)
        return entry

# --------------------------------------------[Functionality Section]--------------------------------------------

    def play_game(self) -> None:
        """
        Start the Cookie Clicker game with the selected options.

        :return: None
        """
        is_bot_on = self.is_bot_on.get()
        is_ratio_on = self.is_ratio_on.get()
        time = self.entry_time.get()
        ratio = self.entry_ratio.get()
        root = self.root
        play_game(is_bot_on, is_ratio_on, time, ratio, root)

    # maybe trigger greying off certain options in the future:
    def bot_options(self) -> None:
        """
        Handler for bot option changes.

        :return: None
        """
        pass
        # print(self.is_bot_on.get())

    # maybe trigger greying off certain options in the future
    def ratio_options(self) -> None:
        """
        Handler for ratio option changes.

        :return: None
        """
        pass
        # print(self.is_ratio_on.get())

