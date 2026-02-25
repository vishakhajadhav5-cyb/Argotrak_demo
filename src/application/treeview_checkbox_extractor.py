from selenium.webdriver.common.by import By
import time, os, pandas as pd

def handle_treeview_checkbox(driver, url, excel_path):
    driver.get(url)
    print("⏳ Please manually select/deselect checkboxes in the browser window...")
    time.sleep(20)  # wait for manual selection

    nodes = driver.find_elements(By.CSS_SELECTOR, "li.e-list-item")
    enabled, disabled = {}, {}

    for node in nodes:
        state = node.get_attribute("aria-checked")
        label = node.find_element(By.CSS_SELECTOR, "span.e-list-text").text.strip()

        try:
            parent = node.find_element(
                By.XPATH, "./ancestor::ul/preceding-sibling::div/span[@class='e-list-text']"
            ).text
        except:
            parent = None

        if parent is None:
            enabled.setdefault(label, [])
            disabled.setdefault(label, [])
        else:
            if state == "true":
                enabled.setdefault(parent, []).append(label)
            elif state == "false":
                disabled.setdefault(parent, []).append(label)
            else:
                enabled.setdefault(parent, []).append(label)

    print("\n📊 Folder Status Summary:\n")
    for folder in sorted(set(enabled.keys()) | set(disabled.keys())):
        e_list = enabled.get(folder, [])
        d_list = disabled.get(folder, [])
        print(f"Folder: {folder}")
        print(f"  Enabled ({len(e_list)}): {', '.join(e_list) if e_list else 'None'}")
        print(f"  Disabled ({len(d_list)}): {', '.join(d_list) if d_list else 'None'}\n")

    # Save to Excel
    rows = []
    all_folders = sorted(set(enabled.keys()) | set(disabled.keys()))
    for folder in all_folders:
        e_list = enabled.get(folder, [])
        d_list = disabled.get(folder, [])
        max_len = max(len(e_list), len(d_list), 1)
        for i in range(max_len):
            rows.append({
                "Folder Name": folder if i == 0 else "",
                "Enabled": e_list[i] if i < len(e_list) else "",
                "Disabled": d_list[i] if i < len(d_list) else ""
            })

    df_new = pd.DataFrame(rows, columns=["Folder Name", "Enabled", "Disabled"])
    if os.path.exists(excel_path):
        existing = pd.read_excel(excel_path)
        final_df = pd.concat([existing, df_new], ignore_index=True)
    else:
        final_df = df_new

    final_df.to_excel(excel_path, index=False)
    print(f"\n✅ Results saved to {excel_path}")
    time.sleep(5)
