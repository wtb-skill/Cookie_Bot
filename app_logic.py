from bot import CookieClickerBot
from clock import Timer
from score import GameScoreManager
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
import threading
import pygetwindow as gw


def play_game(is_bot_on: int, is_ratio_on: int, time: str, ratio: str, root: tk.Tk) -> None:
    """
    Start the Cookie Clicker game with the selected options.

    :param is_bot_on: Indicates whether the bot is enabled (1 for on, 2 for off).
    :type is_bot_on: int
    :param is_ratio_on: Indicates whether the ratio option is enabled (1 for on, 2 for off).
    :type is_ratio_on: int
    :param time: Duration of the game in seconds.
    :type time: str
    :param ratio: The ratio for upgrade buying.
    :type ratio: str
    :param root: The main Tkinter root window.
    :type root: tk.Tk
    :return: None
    """
    duration = int(time)  # duration of the game
    ratio = float(ratio)

    # Create and start the timer
    timer_window = tk.Toplevel(root)
    timer = Timer(timer_window)

    # Function to check when the webpage window is active and start the timer
    def start_timer_when_webpage_active():
        webpage_window = gw.getWindowsWithTitle("0 cookies - Cookie Clicker")
        if webpage_window and webpage_window[0].isActive:
            timer_thread = threading.Thread(target=timer.count_down, args=(duration,))
            timer_thread.start()
        else:
            root.after(100, start_timer_when_webpage_active)

    # Start checking for webpage activity
    start_timer_when_webpage_active()

    # Start the game in a separate thread
    game_thread = threading.Thread(target=start_game, args=(is_bot_on, is_ratio_on, duration, ratio, timer_window))
    game_thread.start()


def start_game(is_bot_on: int, is_ratio_on: int, duration: int, ratio: float, timer_window: tk.Toplevel) -> None:
    """
    Start the Cookie Clicker game based on selected options.

    :param is_bot_on: Indicates whether the bot is enabled (1 for on, 2 for off).
    :type is_bot_on: int
    :param is_ratio_on: Indicates whether the ratio option is enabled (1 for on, 2 for off).
    :type is_ratio_on: int
    :param duration: Duration of the game in seconds.
    :type duration: int
    :param ratio: The ratio for upgrade buying.
    :type ratio: float
    :param timer_window: The timer window for displaying the game duration.
    :type timer_window: tk.Toplevel
    :return: None
    """
    try:
        if is_bot_on == 2 and is_ratio_on == 2:
            bot = CookieClickerBot(click_enabled=False, ratio_enabled=False)
            bot.game(duration=duration)
        elif is_bot_on == 2 and is_ratio_on == 1:  # ERROR after first upgrade
            bot = CookieClickerBot(click_enabled=False, ratio_enabled=True)
            bot.game(duration=duration, ratio=ratio)
        elif is_bot_on == 1 and is_ratio_on == 2:
            bot = CookieClickerBot(click_enabled=True, ratio_enabled=False)
            bot.game(duration=duration)
        elif is_bot_on == 1 and is_ratio_on == 1:
            bot = CookieClickerBot(click_enabled=True, ratio_enabled=True)
            bot.game(duration=duration, ratio=ratio)
    except Exception:
        messagebox.showinfo("Game Aborted", "The game was aborted because the webpage was closed.")
        timer_window.destroy()


def show_leaderboard(root: tk.Tk) -> None:
    """
    Display the leaderboard in a new window.

    :param root: The main Tkinter root window.
    :type root: tk.Tk
    :return: None
    """
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")

    score_manager = GameScoreManager()
    leaderboard_data = score_manager.get_leaderboard()

    tree = ttk.Treeview(leaderboard_window, columns=('CPS', 'Time', 'Mode'))
    tree.heading("#1", text="CPS", command=lambda: sort_column(tree, "CPS", False))
    tree.heading("#2", text="Time", command=lambda: sort_column(tree, "Time", False))
    tree.heading("#3", text="Mode", command=lambda: sort_column(tree, "Mode", False))

    for index, row in leaderboard_data.iterrows():
        cps = row['CPS']
        time = row['Time']
        mode = row['Mode']
        tree.insert("", tk.END, values=(cps, time, mode))

    tree.pack()


def sort_column(tree: ttk.Treeview, col: str, reverse: bool) -> None:
    """
    Sort the leaderboard table by a column.

    :param tree: The Treeview widget containing the leaderboard table.
    :type tree: ttk.Treeview
    :param col: The column to sort by.
    :type col: str
    :param reverse: Indicates whether to reverse the sorting order.
    :type reverse: bool
    :return: None
    """
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    data.sort(reverse=reverse)

    for index, item in enumerate(data):
        tree.move(item[1], '', index)

    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))


def show_help(root: tk.Tk) -> None:
    """
    Display a help message in a new window.

    :param root: The main Tkinter root window.
    :type root: tk.Tk
    :return: None
    """
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.resizable(False, False)  # user unable to change the size of the window

    text_help = tk.Text(help_window, wrap=tk.WORD, width=90, height=11, background="Light Steel Blue")

    def insert_bold_label(text_widget: tk.Text, label: str, description: str) -> None:
        """
        Insert a bold label followed by a description into a Tkinter Text widget.

        :param text_widget: The Tkinter Text widget where the text should be inserted.
        :type text_widget: tk.Text
        :param label: The label text to be displayed in bold.
        :type label: str
        :param description: The description text to be displayed.
        :type description: str
        :return: None
        """
        text_widget.tag_configure("bold", font=("FreeMono", 10, "bold"))
        text_widget.insert(tk.END, f"{label}:", "bold")
        text_widget.insert(tk.END, f" {description}\n")

    insert_bold_label(text_help, "Cookie", "Starts the app with chosen options.")
    insert_bold_label(text_help, "Clicker", "Assigns the bot to click the cookie for you.")
    insert_bold_label(text_help, "Buy-Out", "Assigns the bot to buy upgrades for you.")
    insert_bold_label(text_help, "Ratio",
                      "Decides how many cheaper upgrades are being bought compared to the more expensive ones.")
    insert_bold_label(text_help, "Time", "Game time in seconds.")
    insert_bold_label(text_help, "Leaderboard",
                      "Displays the leaderboard. You can sort it by CPS(cookies per second), time or game mode "
                      "(ratio or manual).")
    insert_bold_label(text_help, "Space",
                      "Pushing the space bar during the game stops/resumes the automated cookie clicking and "
                      "upgrade buying.")

    text_help.pack(padx=10, pady=10)


