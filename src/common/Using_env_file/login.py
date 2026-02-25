import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv   # ✅ added
import time
import os

# Load environment variables
load_dotenv()

# Path to JSON file
JSON_PATH = os.path.join("C:\\Users\\vishakhajad\\Desktop\\ArgoTrak_Project\\PageObject", "Login_Page.json")

# Load locators
with open(JSON_PATH, "r") as f:
    locators = json.load(f)

class ArgoTrakLogin:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def check_and_interact(self, by_type, locator, value=None, action="send_keys"):
        try:
            element = self.driver.find_element(by_type, locator)
            if element.is_displayed():
                element.clear()
                print(f"Element visible: {locator}")
                if action == "send_keys" and value is not None:
                    element.send_keys(value)
                elif action == "click":
                    element.click()
                elif action == "select" and value is not None:
                    Select(element).select_by_visible_text(value)
            else:
                print(f"Element NOT visible: {locator}")
        except NoSuchElementException:
            print(f"Element NOT found: {locator}")

    def click_checkbox_if_not_selected(self, by_type, locator):
        try:
            element = self.driver.find_element(by_type, locator)
            if element.is_displayed():
                if not element.is_selected():
                    element.click()
                    print(f"Checkbox clicked: {locator}")
                else:
                    print(f"Checkbox already selected: {locator}")
            else:
                print(f"Checkbox NOT visible: {locator}")
        except NoSuchElementException:
            print(f"Checkbox NOT found: {locator}")

    def login(self):
        # Username
        self.check_and_interact(By.XPATH, locators["username"]["value"], self.username)

        # Password
        self.check_and_interact(By.XPATH, locators["password"]["value"], self.password)

        # Remember password
        self.click_checkbox_if_not_selected(By.XPATH, locators["remember"]["value"])

        # Login button
        # self.check_and_interact(By.XPATH, locators["login_btn"]["value"], action="click")


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://argotrak.org/")
    time.sleep(5)

    # ✅ Load credentials from .env
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    login_bot = ArgoTrakLogin(driver, username, password)
    login_bot.login()

    time.sleep(5)
    driver.quit()
