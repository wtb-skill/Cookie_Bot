from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from score import GameScoreManager
import time
import keyboard
from typing import List


class CookieClickerBot:
    """
    A bot for automating gameplay in the Cookie Clicker web game using Selenium.
    """
    def __init__(self, ratio_enabled: bool, click_enabled: bool):
        """
        Initialize the CookieClickerBot instance.

        :param ratio_enabled: Indicates whether the bot should use the ratio for upgrades.
        :type ratio_enabled: bool
        :param click_enabled: Indicates whether clicking functionality is enabled.
        :type click_enabled: bool
        """
        self.bot_mode: str = "automated"  # Start in automated mode
        self.click_enabled = click_enabled
        self.ratio_enabled = ratio_enabled  # changes ratio use
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')  # no open window
        # self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("http://orteil.dashnet.org/experiments/cookie/")

        keyboard.on_press_key("space", self.toggle_bot_mode)  # Hook the space key to toggle bot mode

    def click(self) -> None:
        """
        Clicks on the cookie element if click functionality is enabled.

        :return: None
        """
        if self.click_enabled:
            cookie: WebElement = self.driver.find_element(By.CSS_SELECTOR, value="div#cookie")
            cookie.click()

    def upgrade(self, upgrade: int) -> None:
        """
        Clicks on a specified upgrade based on the index.

        :param upgrade: Index of the upgrade to be clicked.
        :type upgrade: int
        :return: None
        """
        upgrades: List[WebElement] = [
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyCursor"),
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyGrandma"),
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyFactory"),
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyMine"),
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyShipment"),
            self.driver.find_element(By.CSS_SELECTOR, value="div[id='buyAlchemy lab']"),
            self.driver.find_element(By.CSS_SELECTOR, value="div#buyPortal"),
            self.driver.find_element(By.CSS_SELECTOR, value="div[id='buyTime machine']")
        ]
        upgrades[upgrade].click()

    def upgrade_cost(self) -> List[int]:
        """
        Retrieve the list of costs for all available upgrades on the webpage.

        This method searches through the webpage and extracts the cost values
        of all available upgrades.

        :return: A list of integers representing the upgrade costs.
        :rtype: list[int]
        """

        upgrade_cost_tags: List[WebElement] = self.driver.find_elements(By.CSS_SELECTOR, value="div#store b")
        upgrade_costs: List[int] = [int(upgrade_cost_tags[i].text.split('- ')[1].replace(",", "")) for i in range(8)]
        return upgrade_costs

    def money_value(self) -> int:
        """
        Retrieve the current money value from the webpage.

        This method searches through the webpage and extracts the current money value.

        :return: The current money value as an integer.
        :rtype: int
        """
        money_tag: str = self.driver.find_element(By.CSS_SELECTOR, value="div#money").text.replace(",", "")
        money = int(money_tag)
        return money

    def ultimate_strategy(self, ratio: float) -> int:
        """
        Determine the index of the next upgrade to buy based on a strategy.

        This method applies a strategy for choosing when and which upgrade to buy in the game.

        :param ratio: A ratio that changes the order of upgrades to be bought.
        :type ratio: float
        :return: The index of the next upgrade to buy.
        :rtype: int
        """
        upgrade_prices: List[int] = self.upgrade_cost()

        """
        # upgrade value = uv:
        increase in cps compared to the previous upgrade, e.g. if 'upgrade 1' increases cps by 0.8 and 
        'upgrade 2' increases cps by 4, the uv[2] = 0.8 * 4 = 5
        """
        uv: List[float] = [1, 4, 5, 2.5, 3.5, 7.14, 20, 123.456789]

        for i in range(len(upgrade_prices) - 1):
            cum: float = 1
            for j in range(len(upgrade_prices) - 1 - i, 0, -1):
                cum *= uv[j]
                if upgrade_prices[j - 1] * cum * ratio <= upgrade_prices[len(upgrade_prices) - 1 - i]:
                    break
                return len(upgrade_prices) - 1 - i
        return 0

    @staticmethod
    def check_money(money: int, next_upgrade_price: int) -> bool:
        """
        Check if you have enough money to buy the next upgrade.

        This method checks if the current amount of money is greater than or equal to
        the cost of the next upgrade.

        :param money: Your current money.
        :type money: int
        :param next_upgrade_price: The cost of the next upgrade.
        :type next_upgrade_price: int
        :return: True if you have enough money, False otherwise.
        :rtype: bool
        """
        return money >= next_upgrade_price

    def score(self) -> float:
        """
        Retrieve the cookies per second (CPS) value from the webpage.

        This method searches through the webpage and extracts the CPS value.

        :return: The CPS value as a floating-point number.
        :rtype: float
        """
        cps_tag: WebElement = self.driver.find_element(By.CSS_SELECTOR, value="div#cps")
        cps = float(cps_tag.text.split(': ')[1])
        return cps

    def toggle_bot_mode(self, event) -> None:
        """
        Toggle the bot mode when the spacebar is pressed.

        This method toggles between 'automated' and 'manual' bot modes based on the
        current mode.

        :param event: The event argument required by the event handling library.
        :type event: Any
        :return: None
        """
        if self.bot_mode == "automated":
            self.bot_mode = "manual"
        else:
            self.bot_mode = "automated"

    def game(self, ratio: float = None, duration: int = 10) -> None:
        """
        This method simulates playing the game for the specified duration (in seconds) while
        applying a chosen ratio for upgrading. It automates clicking and upgrading based on
        the bot mode and chosen ratio.

        :param ratio: The ratio that changes the order of upgrades (default is None).
        :type ratio: float or None
        :param duration: The duration of the game in seconds (default is 10 seconds).
        :type duration: int
        :return: None
        """
        start_time: float = time.time()
        end_time = start_time + duration

        while time.time() < end_time:  # for the game duration:
            if self.bot_mode == "automated":  # click if Clicker ON
                self.click()
            try:  # handles StaleElementReferenceException, which happens when Clicker off and Ratio ON
                if self.ratio_enabled:  # buy upgrades if Ration ON
                    next_upgrade = self.ultimate_strategy(ratio)
                    if self.check_money(self.money_value(), next_upgrade):
                        self.upgrade(next_upgrade)
            except StaleElementReferenceException:
                pass

        score_manager = GameScoreManager()  # save the score
        score_manager.add_score(self.score(), duration, ratio)  # save the score

        print(f"Cookies/Second: {self.score()}, Money: {self.money_value()}")
        self.driver.quit()

    def __del__(self) -> None:
        """
        Clean up and unhook the keyboard event handler when the bot is deleted.

        This method is automatically called when the CookieClickerBot object is deleted.
        It ensures that the keyboard event handler is unhooked to prevent resource leaks.

        :return: None
        """
        keyboard.unhook_all()

