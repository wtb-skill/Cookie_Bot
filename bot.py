from selenium import webdriver
from selenium.webdriver.common.by import By
from score import GameScoreManager
import time
import keyboard



class CookieClickerBot:
    def __init__(self, ratio_enabled, click_enabled):  # changes ratio use
        self.bot_mode = "automated"  # Start in automated mode
        self.click_enabled = click_enabled
        self.ratio_enabled = ratio_enabled  # changes ratio use
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("http://orteil.dashnet.org/experiments/cookie/")

        keyboard.on_press_key("space", self.toggle_bot_mode)  # Hook the space key to toggle bot mode

    def click(self):
        """
        Click on a cookie.
        """
        if self.click_enabled:
            cookie = self.driver.find_element(By.CSS_SELECTOR, value="div#cookie")
            cookie.click()

    def upgrade(self, upgrade):
        """
        Click on the upgrade.
        :param upgrade: chosen upgrade
        """
        upgrades = [
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

    def upgrade_cost(self):
        """
        Searches through the webpage for the list of all upgrade costs.
        :return: the list of all upgrade costs
        """

        upgrade_cost_tags = self.driver.find_elements(By.CSS_SELECTOR, value="div#store b")
        upgrade_costs = [int(upgrade_cost_tags[i].text.split('- ')[1].replace(",", "")) for i in range(8)]
        return upgrade_costs

    def money_value(self):
        """
        Searches through the webpage for the money value.
        :return: the money value
        """
        money_tag = self.driver.find_element(By.CSS_SELECTOR, value="div#money").text.replace(",", "")
        money = int(money_tag)
        return money

    def ultimate_strategy(self, ratio):
        """
        The applied strategy for the game regarding when and which upgrade to buy.
        :param ratio: changes the order in which the upgrades are being bought out
        :return: the index of the next upgrade to buy
        """
        upgrade_prices = self.upgrade_cost()

        # upgrade value:
        uv = [1, 4, 5, 2.5, 3.5, 7.14, 20, 123.456789]  # increase in cps compared to the previous upgrade
        # e.g. if 'upgrade 1' increases cps by 0.8 and 'upgrade 2' increases cps by 4, the uv[2] = 5

        for i in range(len(upgrade_prices) - 1):
            cum = 1
            for j in range(len(upgrade_prices) - 1 - i, 0, -1):
                cum *= uv[j]
                if upgrade_prices[j - 1] * cum * ratio <= upgrade_prices[len(upgrade_prices) - 1 - i]:
                    break
                return len(upgrade_prices) - 1 - i
        return 0

    @staticmethod
    def check_money(money, next_upgrade_price):
        """
        Checks if you have enough money to buy the next upgrade.
        :param money: your current money
        :param next_upgrade_price: the cost the next upgrade
        :return: bool
        """
        return money >= next_upgrade_price

    def score(self):
        """
        Searches through the webpage for the cookies per second value.
        :return: cookies/second value
        """
        cps_tag = self.driver.find_element(By.CSS_SELECTOR, value="div#cps")
        cps = float(cps_tag.text.split(': ')[1])
        return cps

    def toggle_bot_mode(self, event):  # event arg is required by the library for the event handling mechanism to work
        """
        Toggle the bot mode when the spacebar is pressed
        """
        if self.bot_mode == "automated":
            self.bot_mode = "manual"
        else:
            self.bot_mode = "automated"

    def game(self, ratio=None, duration=10):  # changes ratio use
        """
        Plays one instance of the game (for the chosen amount of seconds) and applies the chosen ratio.
        :param ratio: changes the order in which the upgrades are being bought out
        :param duration: duration of the game in seconds (default is 10 seconds)
        :return:
        """
        start_time = time.time()
        end_time = start_time + duration

        # OLD:
        while time.time() < end_time:
            if self.bot_mode == "automated":
                self.click()
                if self.ratio_enabled:
                    next_upgrade = self.ultimate_strategy(ratio)
                    if self.check_money(self.money_value(), next_upgrade):
                        self.upgrade(next_upgrade)

        score_manager = GameScoreManager()  # save the score
        score_manager.add_score(self.score(), duration, ratio)  # save the score

        print(f"Cookies/Second: {self.score()}, Money: {self.money_value()}")
        self.driver.quit()

    def __del__(self):
        """
        Clean up and unhook the keyboard event handler when the bot is deleted
        :return:
        """
        keyboard.unhook_all()

