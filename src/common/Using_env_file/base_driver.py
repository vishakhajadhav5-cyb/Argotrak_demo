from selenium import webdriver
import json
import os

class BaseDriver:
    def __init__(self, config_path='config/config.json'):
        with open(config_path) as f:
            self.config = json.load(f)
        self.driver = None

    def open_browser(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(self.config['url'])
        return self.driver

    def close_browser(self):
        if self.driver:
            self.driver.quit()
