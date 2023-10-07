from tkinter import *
import math


class Timer:
    """
    A simple countdown timer GUI using Tkinter.
    """

    FONT_NAME = "Courier"

    def __init__(self, root: Tk):
        """
        Initialize the Timer instance.

        :param root: The Tkinter root window.
        :type root: Tk
        """
        self.root = root
        self.root.title("Timer")

        # Get the screen width and height
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Calculate the desired window position and size
        self.window_width = 200
        self.window_height = 200
        self.window_x = self.screen_width - self.screen_height + 400  # Place it closer to the right side
        self.window_y = 50  # Place it closer to the top

        # Set the window's geometry
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")

        # Set the canvas
        self.canvas = Canvas(root, width=200, height=200, bg='black', highlightthickness=0)
        self.timer_text = self.canvas.create_text(
            self.window_width // 2,
            self.window_height // 2,
            fill="white",
            text="00:00",
            font=(self.FONT_NAME, 35, "bold")
        )
        self.canvas.grid(row=0, column=0, padx=0, pady=0)

    def count_down(self, count: int):
        """
        Start the countdown timer.

        :param count: The countdown time in seconds.
        :type count: int
        """
        count_min = math.floor(count / 60)
        count_sec = count % 60

        if count_sec < 10:
            count_sec = f"0{count_sec}"

        self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
        if count > 0:
            self.root.after(1000, self.count_down, count - 1)
        else:
            self.root.destroy()

