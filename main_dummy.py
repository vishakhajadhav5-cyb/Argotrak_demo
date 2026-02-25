import json
from utils.common.browser_manager import launch_browser
from src.application.star_arrow_handle import handle_star_arrow
from src.application.treeview_checkbox_extractor import handle_treeview_checkbox
import sys
import os
from src.common.base_driver import BaseDriver
from src.application.maintenance import MaintenancePage
from src.application.alerts import AlertsPage
# ==============================
# Load Configuration
# ==============================
with open("config/config_dummy.json", "r") as f:
    config = json.load(f)

# ==============================
# 1️⃣ Run Star Arrow Test
# ==============================
print("\n🚀 Running Star Arrow HTML automation...")
star_conf = config["star_arrow"]
driver = launch_browser(star_conf["browser"], star_conf.get("chrome_options"))
handle_star_arrow(driver, star_conf["html_file_path"])
driver.quit()

# ==============================
# 2️⃣ Run Treeview Checkbox Test
# ==============================
print("\n🌳 Running Treeview Checkbox automation...")
tree_conf = config["treeview"]
driver = launch_browser(tree_conf["browser"])
handle_treeview_checkbox(driver, tree_conf["url"], tree_conf["excel_path"])
driver.quit()

print("\n✅ All automation scripts executed successfully!")
