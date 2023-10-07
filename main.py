from gui import CookieClickerBotApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieClickerBotApp(root)

    root.mainloop()

# works, to find optimal ratio:
# if __name__ == "__main__":
#
#     ratio = 0.5
#
#     while ratio <= 1:
#         bot = CookieClickerBot()
#         bot.game(ratio=ratio)  # Adjust the ratio as
#         print("-----------------")
#         # time.sleep(15)
#         ratio += 0.05


# TODO 2✔️: Add saving of score. Both to the file and displaying in the GUI.
#         - Message displaying after 1 game instance- not sure if needed.
#         - I have 3(4) game modes now, need to change the score
# TODO 4: Maybe a dev like mode to find the perfect value of ratio for a given time.
# TODO 5: Make this app function outside of pycharm. Problem finding Selenium module.
# TODO 7: Edit the code with notes, explanations, etc.
# TODO 8: Fix naming of functions, variables, etc, check for unnecessary elements.
# TODO 10✔: Add manual game without bot and ratio (and allow score).
#          - Clicker OFF, Buy-Out ON provides error, StaleElement, rest works
#          - Either fix it or change the code to only allow 3 modes.

# C:\Users\adamb\Downloads\chromedriver-win64\chromedriver-win64
# cd C:\Python nauka\Cookie_Bot
# python -m PyInstaller --onefile --add-data "C:\Users\adamb\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe;." --add-data "C:\Python nauka\Cookie_Bot\venv\Lib\site-packages\selenium;." main.py
# python -m PyInstaller --onefile --add-binary "C:\Users\adamb\Downloads\chromedriver-win64\chromedriver.exe;." main.py
# python -m PyInstaller --onefile --add-data "C:\Users\adamb\Downloads\chromedriver-win64\chromedriver-win64.exe;." --add-data "path\to\selenium\package;selenium" main.py

