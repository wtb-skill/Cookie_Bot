# Cookie Clicker Bot

A Cookie Clicker Bot that automates gameplay in the popular web game Cookie Clicker. This bot can automatically click 
cookies, purchase upgrades, and apply strategic buying ratios for upgrades based on user input. The project integrates 
web automation using Selenium, a graphical user interface (GUI) built with Tkinter, and a timer to track game duration.
It also features a leaderboard to display high scores and a help section to guide users in using the bot.

## Features

- 🍪 Cookie Clicking Automation – Automatically clicks the cookie in the Cookie Clicker game to increase cookies per second (CPS).
- 💡 Upgrade Purchasing – Buys available upgrades using a custom strategy that can prioritize cheaper or more expensive upgrades based on a user-defined ratio.
- ⏲️ Game Timer – Tracks and displays the duration of the game, providing real-time updates.
- 🎮 Manual/Automated Mode – Toggle between automated gameplay or manual control using the spacebar.
- 📊 Leaderboard – Displays a leaderboard with high scores, allowing sorting by CPS, time, and game mode.
- 📱 GUI Interface – Built with Tkinter, providing an intuitive interface for users to interact with the bot and adjust settings.
- ⚙️ Customization – Users can set the duration of the game and customize the upgrade buying strategy with a ratio (e.g., prioritizing cheaper or more expensive upgrades).
- 🎮 Bot Mode Toggle – Allows users to switch between fully automated gameplay and manual control during the game.
- 🧱 Modular Codebase – Organized into separate modules for game logic, GUI, and bot control for easy customization and extension.

## Project Structure

```
├── main.py                     # Entry point for starting the GUI and bot
│
├── core/                       # Core application logic and bot functionalities
│   ├── app_logic.py            # Core logic for game management and control
│   ├── bot.py                  # CookieClickerBot class handling clicking and upgrading
│   ├── clock.py                # Timer implementation for game duration
│   └── score.py                # Handles score tracking and leaderboard management
│
├── gui/                        # GUI components and related assets
│   ├── gui.py                  # GUI implementation using Tkinter
│   └── cookie.png              # Icon or logo used in the GUI
│
├── data/                       # Data files and saved game scores
│   └── score.csv               # Stores game scores and performance metrics
│
├── README.md                   # Project description, features, and usage instructions
├── requirements.txt            # Dependencies required to run the project
└── .gitignore                  # Excludes unnecessary files from version control

```

## Usage

### 1. Install Project Dependencies

Start by installing the required Python dependencies. You can install them using `pip` from the `requirements.txt` file.

```
pip install -r requirements.txt
```

### 2. Run the Application

To start the application, run the following command:
```
python main.py
```
The app will launch a Tkinter UI.

## Authors

    Adam Bałdyga

## License

This project is licensed under the MIT License.
