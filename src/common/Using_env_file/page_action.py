from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PageActions:
    def __init__(self, driver):
        self.driver = driver

    def click(self, by_type, selector):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by_type, selector))).click()

    def send_keys(self, by_type, selector, value):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_type, selector))).send_keys(value)

    def get_text(self, by_type, selector):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by_type, selector))).text

    def wait_for_element(self, by_type, selector, timeout=10):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by_type, selector)))
