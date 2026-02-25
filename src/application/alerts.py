from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
from src.common.page_actions import PageActions


class AlertsPage:
    def __init__(self, driver, excel_manager):
        self.driver = driver
        self.action = PageActions(driver)
        self.excel = excel_manager  # Excel manager instance

    def open_tab(self):
        """Open Alerts tab in UI"""
        self.action.click(By.XPATH, "//button[text()='Alerts']")
        time.sleep(1)

    def process_star_or_admin_rows(self):
        """Iterate alerts table and process rows with ⭐ or Administrator"""
        print("🔍 Scanning Alerts table for ⭐ or Administrator...")
        rows = self.driver.find_elements(By.XPATH, "//table[@id='alertTable']/tbody/tr")
        if not rows:
            print("⚠️ No rows found in Alerts table!")
            return

        for index, row in enumerate(rows, start=1):
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 3:
                    continue

                star_cell = cells[0].text.strip()
                admin_cell = cells[-1].text.strip()

                # ✅ process if star or administrator
                if star_cell == "⭐" or admin_cell.lower() == "administrator":
                    print(f"✅ Match found at row {index}")

                    # Extract Group Name
                    group_name = cells[2].text.strip() if len(cells) > 2 else "N/A"

                    # Click forward button
                    forward_button = row.find_element(By.CSS_SELECTOR, "button.forward")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", forward_button)
                    WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(forward_button))
                    forward_button.click()
                    print("👉 Forward button clicked successfully!")

                    # Wait for popup
                    try:
                        WebDriverWait(self.driver, 5).until(
                            EC.visibility_of_element_located((By.ID, "userSelectorPopup"))
                        )
                        self.extract_user_selector_data(group_name)
                    except TimeoutException:
                        print("⚠️ Popup did not appear after clicking → button.")
                    break  # remove this `break` if you want to process all rows

            except NoSuchElementException as e:
                print(f"⚠️ Element issue in row {index}: {e}")

        print("✅ Finished processing Alerts table.")

    def extract_user_selector_data(self, group_name):
        """Extract popup alert details and save to Excel"""
        try:
            popup = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, "userSelectorPopup"))
            )

            # Extract Alert Name (Copy Alert)
            alert_name_raw = popup.find_element(By.XPATH, ".//tr[1]/td[2]/input").get_attribute("value").strip()
            print(f"🔔 Raw Alert Name Found: {alert_name_raw}")

            # ✅ If no "*" in alert name → save all as "NA" except group
            if "*" not in alert_name_raw:
                print("⚠️ Alert name does not contain '*', saving 'NA' for all fields.")
                row_data = [group_name] + ["NA"] * 7  # 8 total columns
                self.excel.append_to_sheet("Alerts", row_data)
                print("✅ NA data written to Excel for non-star alert.\n")
                popup.find_element(By.XPATH, ".//button[contains(text(),'Close')]").click()
                return

            # ✅ Remove "*" before saving
            alert_name = alert_name_raw.replace("*", "").strip()

            # Extract popup field values
            ignore_duplicates = popup.find_element(By.XPATH, ".//tr[2]/td[2]/input").get_attribute("value").strip()
            threshold_value = popup.find_element(By.XPATH, ".//tr[3]/td[2]/input").get_attribute("value").strip()

            # Extract checked days
            # ✅ Extract only checked checkboxes' labels (for Scheduled Days)
            checked_boxes = self.driver.find_elements(
                By.XPATH, "//div[@id='userSelectorPopup']//label/input[@type='checkbox' and @checked]"
            )

            checked_items = []
            for box in checked_boxes:
                # Get the text inside the parent label (e.g., "Mon", "Wed")
                label_text = self.driver.execute_script("""
                    return arguments[0].parentNode.textContent.trim();
                """, box)
                if label_text:
                    checked_items.append(label_text)

            # Join into a comma-separated string or use "N/A" if none are checked
            scheduled_days = ", ".join(checked_items) if checked_items else "N/A"

            print("📅 Scheduled Days:", scheduled_days)
            start_time = popup.find_element(By.XPATH, "//*[@id='userSelectorPopup']/table/tbody/tr[5]/td[2]/input").get_attribute("value").strip()
            end_time = popup.find_element(By.XPATH,"//*[@id='userSelectorPopup']/table/tbody/tr[6]/td[2]/input").get_attribute("value").strip()
            delivery_email = popup.find_element(By.XPATH, ".//tr[6]/td[2]/input").get_attribute("value").strip()
            delivery_type = popup.find_element(By.XPATH, ".//tr[7]/td[2]/input").get_attribute("value").strip()

            # Prepare Excel row
            row_data = [
                group_name,
                alert_name,
                ignore_duplicates,
                threshold_value,
                scheduled_days,
                start_time,
                end_time,
                f"{delivery_email} ({delivery_type})"
            ]

            print("\n📋 Extracted Alert Popup Data:")
            headers = [
                "Group Name", "Alert Name", "Ignore Duplicates (min)", "Threshold (nmi)",
                "Scheduled Days", "Start Time", "End Time", "Delivery Action"
            ]
            for h, v in zip(headers, row_data):
                print(f"   {h}: {v}")

            # ✅ Save data to Excel
            self.excel.append_to_sheet("Alerts", row_data)
            print("✅ Data written successfully to Excel 'Alerts' sheet.")

            # Close popup
            popup.find_element(By.XPATH, ".//button[contains(text(),'Close')]").click()
            print("✅ Popup closed successfully.\n")

        except Exception as e:
            print(f"⚠️ Error extracting popup data: {e}")
