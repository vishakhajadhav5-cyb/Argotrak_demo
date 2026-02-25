# credentials_checkbox_tree.py
from robot.libraries.BuiltIn import BuiltIn

def extract_checked_tree_labels():
    try:
        sl = BuiltIn().get_library_instance('SeleniumLibrary')
        driver = sl.driver

        checked_boxes = driver.find_elements(
            "xpath", "//div[@id='credentials']//ul[@class='tree']//input[@type='checkbox' and @checked]"
        )

        checked_items = []
        for box in checked_boxes:
            label_text = driver.execute_script("""
                const next = arguments[0].nextSibling;
                if (next && next.nodeType === Node.TEXT_NODE) return next.textContent.trim();
                const lbl = arguments[0].closest('label');
                if (lbl) return lbl.textContent.trim();
                return '';
            """, box)
            if label_text:
                checked_items.append(label_text.strip())

        return ", ".join(checked_items)

    except Exception as e:
        print(f"⚠️ Error extracting checked items: {e}")
        return ""
