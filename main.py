import sys, os, traceback
from datetime import datetime
from utils.common.excel_manager import ExcelManager
from src.common.base_driver import BaseDriver
from src.application.alerts import AlertsPage
from src.application.reports import ReportsPage
from src.application.maindevicelistpage import MainDeviceListPage
from src.application.maintenance import MaintenancePage
from src.application.credentials import CredentialsPage
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

RESULT_FOLDER = os.path.join(project_root, "results", "output")
RESULT_FILE_PATH = os.path.join(RESULT_FOLDER, "ArgoTrak_Results.xlsx")
os.makedirs(RESULT_FOLDER, exist_ok=True)

def log_result(excel_manager, module_name, status, message=""):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    excel_manager.append_to_sheet("Results", [now, module_name, status, message])
    print(f"🟢 Logged {module_name} → {status}")

if __name__ == "__main__":
    print("🚀 Starting ArgoTrak automation...")

    # Excel setup
    excel_manager = ExcelManager(RESULT_FILE_PATH)
    excel_manager.ensure_sheets()
    print(f"✅ Excel setup ready at: {RESULT_FILE_PATH}")

    # Browser
    base = BaseDriver()
    driver = base.open_browser()

    try:
        # Main Device List
        try:
            device_page = MainDeviceListPage(driver, excel_manager)
            device_page.perform_device_list_actions()
            log_result(excel_manager, "Main Device List", "PASS")
        except Exception as e:
            log_result(excel_manager, "Main Device List", "FAIL", str(e))

        # # Alerts
        alerts = AlertsPage(driver, excel_manager)
        alerts.open_tab()
        alerts.process_star_or_admin_rows()
        log_result(excel_manager, "Alerts Page", "PASS")

        # # Reports
        reports = ReportsPage(driver, excel_manager)
        reports.open_tab()
        reports.process_reports()
        log_result(excel_manager, "Reports Page", "PASS")

        # Maintenance
        # 3️⃣ MAINTENANCE PAGE
        try:
            print("\n➡️ Navigating: Maintenance Page")
            maintenance = MaintenancePage(driver, excel_manager)
            maintenance.open_tab()  # if tab click is needed
            maintenance.open_maintenance_manager()
            log_result(excel_manager, "Maintenance Page", "PASS")
        except Exception as e:
            error_msg = traceback.format_exc(limit=1)
            print(f"❌ Maintenance Page failed: {e}")
            log_result(excel_manager, "Maintenance Page", "FAIL", error_msg)


        # 3️⃣ credentials
        try:
            print("\n➡️ Navigating: Credentials Page")
            credentials = CredentialsPage(driver, excel_manager)
            credentials.open_tab()  # if tab click is needed
            credentials.open_manage_user_group_access()
            log_result(excel_manager, "Credentials Page", "PASS")
        except Exception as e:
            error_msg = traceback.format_exc(limit=1)
            print(f"❌ Credentials Page failed: {e}")
            log_result(excel_manager, "Credentials Page", "FAIL", error_msg)

    except Exception as e:
        print(f"🔥 Critical error: {e}")

    finally:
        base.close_browser()
        print("🧹 Browser closed. Run complete.")
