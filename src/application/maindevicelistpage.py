# # src/application/main_device_list.py
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
# import time

# class MainDeviceListPage:
#     """Page object for Main Device List tab."""

#     def __init__(self, driver):
#         self.driver = driver

#         # Locators
#         self.main_device_tab = (By.XPATH, "//button[contains(text(),'Main Device List')]")
#         self.download_button = (By.XPATH, "//button[contains(text(),'Download') or contains(@id,'download')]")

#     def open_main_device_tab(self):
#         """Click on Main Device List tab."""
#         try:
#             tab = self.driver.find_element(*self.main_device_tab)
#             tab.click()
#             print("✅ Clicked on 'Main Device List' tab successfully.")
#             time.sleep(2)
#         except NoSuchElementException:
#             print("❌ Main Device List tab not found.")
#         except ElementNotInteractableException:
#             print("⚠️ Main Device List tab not clickable at the moment.")

#     def click_download_if_visible(self):
#         """Check if the Download button is visible, then click it."""
#         try:
#             download_btn = self.driver.find_element(*self.download_button)
#             if download_btn.is_displayed() and download_btn.is_enabled():
#                 download_btn.click()
#                 print("✅ Download button clicked successfully.")
#             else:
#                 print("⚠️ Download button is not visible or not enabled.")
#         except NoSuchElementException:
#             print("❌ Download button not found on the page.")
#         except ElementNotInteractableException:
#             print("⚠️ Download button found but not clickable.")

#     def perform_device_list_actions(self):
#         """Wrapper method to perform both actions together."""
#         self.open_main_device_tab()
#         time.sleep(2)
#         self.click_download_if_visible()

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time

class MainDeviceListPage:
    """Page object for Main Device List tab."""

    def __init__(self, driver, excel_manager=None):
        self.driver = driver
        self.excel = excel_manager  # Optional Excel manager instance

        # Locators
        self.main_device_tab = (By.XPATH, "//button[contains(text(),'Main Device List')]")
        self.download_button = (By.XPATH, "//button[contains(text(),'Download') or contains(@id,'download')]")
        self.device_table = (By.XPATH, "//table[@id='deviceTable']")

    # ----------------------- TAB OPEN -----------------------
    def open_main_device_tab(self):
        """Click on Main Device List tab."""
        try:
            tab = self.driver.find_element(*self.main_device_tab)
            tab.click()
            print("✅ Clicked on 'Main Device List' tab successfully.")
            time.sleep(2)
        except NoSuchElementException:
            print("❌ Main Device List tab not found.")
        except ElementNotInteractableException:
            print("⚠️ Main Device List tab not clickable at the moment.")

    # ----------------------- DOWNLOAD BUTTON -----------------------
    def click_download_if_visible(self):
        """Check if the Download button is visible, then click it."""
        try:
            download_btn = self.driver.find_element(*self.download_button)
            if download_btn.is_displayed() and download_btn.is_enabled():
                download_btn.click()
                print("✅ Download button clicked successfully.")
            else:
                print("⚠️ Download button is not visible or not enabled.")
        except NoSuchElementException:
            print("❌ Download button not found on the page.")
        except ElementNotInteractableException:
            print("⚠️ Download button found but not clickable.")

    # ----------------------- TABLE EXTRACTION -----------------------
    def extract_device_table_data(self):
        """Extracts device list table data and saves it to Excel."""
        try:
            print("🔍 Extracting data from Main Device List table...")

            # Locate the table
            table = self.driver.find_element(*self.device_table)
            rows = table.find_elements(By.XPATH, ".//tbody/tr")

            if not rows:
                print("⚠️ No rows found in device table.")
                return

            print(f"📦 Found {len(rows)} rows in the device table.")

            for row in rows:
                cols = [td.text.strip() for td in row.find_elements(By.TAG_NAME, "td")]
                if cols:
                    print(f"   → Row data: {cols}")
                    if self.excel:
                        self.excel.append_to_sheet("MainDeviceList", cols)

            if self.excel:
                print("✅ Device table data written to Excel (MainDeviceList sheet).")
            else:
                print("ℹ️ Excel manager not provided — data printed only.")

        except NoSuchElementException:
            print("❌ Device table not found on the page.")
        except Exception as e:
            print(f"⚠️ Error extracting device table data: {e}")

    # ----------------------- MASTER FUNCTION -----------------------
    def perform_device_list_actions(self):
        """Wrapper method to open tab, click download, and extract table."""
        self.open_main_device_tab()
        time.sleep(2)
        self.click_download_if_visible()
        time.sleep(2)
        self.extract_device_table_data()
