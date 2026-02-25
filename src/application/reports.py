from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from src.common.page_actions import PageActions
class ReportsPage:
    def __init__(self, driver, excel_manager):
        self.driver = driver
        self.action = PageActions(driver)
        self.excel = excel_manager  # same ExcelManager instance

    def open_tab(self):
        self.action.click(By.XPATH, "//button[text()='Reports']")
        time.sleep(1)

    def process_reports(self):
        print("🔍 Scanning Reports cards for Scheduled entries...")
        report_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.report-card")
        if not report_cards:
            print("⚠️ No report cards found!")
            return

        for card in report_cards:
            text = card.text.lower()
            if "scheduled" in text:
                try:
                    button = card.find_element(By.CSS_SELECTOR, "button.btn")
                    button.click()
                    WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.ID, "schedulerPopup"))
                    )
                    self.extract_scheduler_data()
                except TimeoutException:
                    print("⚠️ Scheduler popup did not appear.")
                break

    def extract_scheduler_data(self):
        try:
            popup = self.driver.find_element(By.ID, "schedulerPopup")
            inputs = popup.find_elements(By.TAG_NAME, "input")

            row_data = [inp.get_attribute("value").strip() for inp in inputs]

            # Print data
            print("\n📋 Extracted Report Scheduler Data:")
            headers = [cell.value for cell in self.excel.wb["Reports"][1]]
            for h, v in zip(headers, row_data):
                print(f"   {h}: {v}")

            # Append to Excel
            self.excel.append_to_sheet("Reports", row_data)
            print("✅ Data written successfully to Excel 'Reports' sheet.")

            # Close popup
            popup.find_element(By.XPATH, ".//button[contains(text(),'Close')]").click()
            print("✅ Popup closed successfully.\n")

        except Exception as e:
            print(f"⚠️ Error extracting scheduler data: {e}")
