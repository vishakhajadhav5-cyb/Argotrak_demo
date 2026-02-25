from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class CredentialsPage:
    def __init__(self, driver, excel_manager):
        self.driver = driver
        self.excel = excel_manager

    def open_tab(self):
        """Click Settings → Tools & Settings"""
        print("🔍 Clicking Settings → Tools & Settings...")
        try:
            settings_icon = self.driver.find_element(By.CSS_SELECTOR, ".nav-icon.settings-icon img")
            settings_icon.click()
            time.sleep(0.5)

            tools_link = self.driver.find_element(
                By.XPATH, "//div[@id='settingsDropdown']//a[contains(text(),'Tools & Settings')]"
            )
            tools_link.click()
            time.sleep(1)
            print("✅ Tools & Settings tab opened")
        except NoSuchElementException as e:
            print(f"⚠️ Settings or Tools & Settings link not found: {e}")

    def open_manage_user_group_access(self):
        """Click Security Tools → Manage User Group Access and extract credentials info"""
        try:
            print("🔍 Clicking 'Security Tools' → 'Manage User Group Access' link...")

            sec_btn = self.driver.find_element(
                By.XPATH, "//*[@id='toolsSettingsTab']//button[contains(text(),'Security Tools')]"
            )
            sec_btn.click()
            time.sleep(0.5)

            manage_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//*[@id='toolsMainContent']/p/a[contains(text(),'Manage User Group Access')]"))
            )
            manage_link.click()
            time.sleep(1)
            print("✅ Manage User Group Access opened")

        except TimeoutException:
            print("⚠️ Manage User Group Access link not found or not clickable")
            return
        except NoSuchElementException:
            print("⚠️ Security Tools button or link not found")
            return

        # ------------------ Extract table and tree data ------------------
        try:
            print("🔍 Extracting Credentials data...")

            # Wait for table
            table = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@id='credentials']//table"))
            )

            rows = table.find_elements(By.TAG_NAME, "tr")
            table_data = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) == 2:
                    val = cols[1].find_element(By.TAG_NAME, "input").get_attribute("value").strip()
                    table_data.append(val)

            print("📋 Form Table Data:")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) == 2:
                    label = cols[0].text.strip()
                    value = cols[1].find_element(By.TAG_NAME, "input").get_attribute("value").strip()
                    print(f"   {label}: {value}")

            # ------------------ Extract tree data ------------------
            # Extract only checked checkboxes' labels (ignore nested unchecked items)
            # ✅ Extract only checked checkboxes' labels (ignore nested unchecked items)
            checked_boxes = self.driver.find_elements(
                By.XPATH, "//div[@id='credentials']//ul[@class='tree']//input[@type='checkbox' and @checked]"
            )

            checked_items = []
            for box in checked_boxes:
                # Get text node immediately following the checkbox (label text)
                label_text = self.driver.execute_script("""
                    const next = arguments[0].nextSibling;
                    return next && next.nodeType === Node.TEXT_NODE ? next.textContent.trim() : '';
                """, box)
                if label_text:
                    checked_items.append(label_text)

            # Convert to comma-separated string
            checked_items_str = ", ".join(checked_items)

            print("📋 Checked Items:")
            print("   " + checked_items_str)

            # ------------------ ✅ Save to Excel ------------------
            # `table_data` should already have your other fields like Full Name, Username, etc.
            self.excel.append_to_sheet("Credentials", table_data + [checked_items_str])
            print("✅ Credentials data written to Excel 'Credentials' sheet (checked only)")

        except TimeoutException:
            print("⚠️ Credentials table or tree did not load")
        except Exception as e:
            print(f"⚠️ Error extracting credentials data: {e}")
