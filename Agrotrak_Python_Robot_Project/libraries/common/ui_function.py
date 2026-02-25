from robot.libraries.BuiltIn import BuiltIn
import time
from selenium.common.exceptions import NoSuchElementException

def open_login(url, username, password):
    """
    Opens the given URL in a browser and performs login.
    Uses the SAME SeleniumLibrary instance that Robot Framework is using.
    """
    print(f"🌐 Opening URL: {url}")
    try:
        # ✅ Get the same SeleniumLibrary instance that Robot uses
        sl = BuiltIn().get_library_instance('SeleniumLibrary')

        sl.open_browser(url, browser="chrome")
        sl.maximize_browser_window()
        time.sleep(1)

        try:
            sl.input_text("id:username", username)
            sl.input_text("id:password", password)
            sl.click_button("id:loginBtn")
            print("✅ Login attempted successfully.")
        except Exception:
            print("ℹ️ No login form found (dummy page). Skipping login.")
        
        return sl  # Return SeleniumLibrary reference

    except Exception as e:
        print(f"❌ Failed to open browser or login: {e}")
        raise

def close_browser_url():
    """Close all open browsers."""
    try:
        sl = BuiltIn().get_library_instance('SeleniumLibrary')
        sl.close_all_browsers()
        print("🧹 Closed all browser sessions.")
    except Exception as e:
        print(f"⚠️ Failed to close browser: {e}")
