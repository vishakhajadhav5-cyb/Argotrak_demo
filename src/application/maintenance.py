from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from src.common.page_actions import PageActions

class MaintenancePage:

    def __init__(self, driver, excel_manager):
        self.driver = driver
        self.action = PageActions(driver)
        self.excel = excel_manager  # shared ExcelManager instance

    def open_tab(self):
   
        print("🔍 Clicking Settings → Tools & Settings...")
        try:
            # Click Settings icon
            settings_icon = self.driver.find_element(By.CSS_SELECTOR, ".nav-icon.settings-icon img")
            settings_icon.click()
            time.sleep(0.5)

            # Click "Tools & Settings" link in dropdown
            tools_link = self.driver.find_element(By.XPATH, "//div[@id='settingsDropdown']//a[contains(text(),'Tools & Settings')]")
            tools_link.click()
            time.sleep(1)
            print("✅ Tools & Settings tab opened")
        except NoSuchElementException as e:
            print(f"⚠️ Settings or Tools & Settings link not found: {e}")


    def open_maintenance_manager(self):
        """Click sidebar button to open Maintenance Manager"""
        try:
            print("🔍 Looking for 'Maintenance Manager' button...")
            btn = self.driver.find_element(By.XPATH, "//*[@id='toolsSettingsTab']/div/div[1]/ul/li[1]/button")
            btn.click()
            print("✅ Maintenance Manager opened")
            time.sleep(1)
            try:
                # Wait for table to appear
                table = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@id='toolsMainContent']//table"))
                )
                rows = table.find_elements(By.TAG_NAME, "tr")
                if len(rows) <= 1:
                    print("⚠️ Maintenance table not visible or empty")
                    return

                print("📋 Extracted Maintenance Table Data:")
                for row in rows[1:]:  # skip header
                    cols = row.find_elements(By.TAG_NAME, "td")
                    data = [col.text.strip() for col in cols]
                    print(f"   {data}")
                    self.excel.append_to_sheet("Maintenance", data)

                print("✅ Maintenance data written to Excel 'Maintenance' sheet")
            except TimeoutException:
                print("⚠️ Maintenance table did not load")
            except Exception as e:
                print(f"⚠️ Error extracting Maintenance data: {e}")
        except NoSuchElementException:
            print("⚠️ Maintenance Manager button not found")
            return False
        return True

    

