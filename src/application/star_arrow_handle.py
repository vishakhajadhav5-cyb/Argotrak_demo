from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
import time

def handle_star_arrow(driver, file_path):
    driver.get(file_path)
    time.sleep(1)

    rows = driver.find_elements(By.XPATH, "//table/tbody/tr[position()>1]")

    for index, row in enumerate(rows, start=2):
        cells = row.find_elements(By.TAG_NAME, "td")

        star_cell = cells[0].text.strip()
        admin_cell = cells[-1].text.strip()

        if star_cell == "⭐" or admin_cell.lower() == "administrator":
            print(f"Found a row with ⭐ at row number: {index}")

            forward_button = row.find_element(By.XPATH, "./td[2]/button")
            print("Forward button element:", forward_button)

            # Click the button
            forward_button.click()
            
            try:
                alert = driver.switch_to.alert
                time.sleep(1)
                print("Alert text:", alert.text)
                alert.accept()
                print("Alert accepted")
            except NoAlertPresentException:
                print("No alert present")

            print("Clicked forward arrow for row:", row.text)
            break

    time.sleep(3)
