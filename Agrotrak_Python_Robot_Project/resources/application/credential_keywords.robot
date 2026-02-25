*** Settings ***
Documentation    🔐 Credentials Manager – Extract user group and permissions data
Library          SeleniumLibrary
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/application/credentials_checkbox_tree.py

*** Keywords ***
Open Tools And Settings Credentials
    [Documentation]    Click on Settings icon → Tools & Settings link
    Log To Console    🔍 Clicking Settings → Tools & Settings...
    ${is_icon}=    Run Keyword And Return Status    Element Should Be Visible    css:.nav-icon.settings-icon img
    Run Keyword If    ${is_icon}    Click Element    css:.nav-icon.settings-icon img
    Sleep    0.5s
    Run Keyword If    ${is_icon}    Click Element    xpath=//div[@id='settingsDropdown']//a[contains(text(),'Tools & Settings')]
    Sleep    1s
    Log To Console    ✅ Tools & Settings tab opened


Open Manage User Group Access
    [Arguments]    ${EXCEL_FILE}
    [Documentation]    Open “Manage User Group Access” under Security Tools and extract credentials info
    Log To Console    🔍 Clicking 'Security Tools' → 'Manage User Group Access' link...

    ${sec_visible}=    Run Keyword And Return Status    Element Should Be Visible    xpath=//*[@id='toolsSettingsTab']//button[contains(text(),'Security Tools')]
    Run Keyword Unless    ${sec_visible}    Log To Console    ⚠️ Security Tools button not visible
    Run Keyword Unless    ${sec_visible}    RETURN

    Click Element    xpath=//*[@id='toolsSettingsTab']//button[contains(text(),'Security Tools')]
    Sleep    0.5s

    ${manage_visible}=    Run Keyword And Return Status    Element Should Be Visible    xpath=//*[@id='toolsMainContent']/p/a[contains(text(),'Manage User Group Access')]
    Run Keyword Unless    ${manage_visible}    Log To Console    ⚠️ Manage User Group Access link not found
    Run Keyword Unless    ${manage_visible}    RETURN

    Click Element    xpath=//*[@id='toolsMainContent']/p/a[contains(text(),'Manage User Group Access')]
    Sleep    1s
    Log To Console    ✅ Manage User Group Access opened
Extract Credentials Data
    [Arguments]    ${EXCEL_FILE}    ${driver}
    [Documentation]    Extract user credentials + checked permissions and write to Excel safely

    ${table_visible}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id='credentials']//table    timeout=5s
    Run Keyword Unless    ${table_visible}    Log To Console    ⚠️ Credentials table did not load
    Run Keyword Unless    ${table_visible}    RETURN

    Log To Console    🔍 Extracting Credentials data...

    # --- Extract table inputs ---
    ${rows}=    Get WebElements    xpath=//div[@id='credentials']//table//tr
    ${table_data}=    Create List
    Log To Console    number of rows:${rows}
    ${row_count}=    Get Length    ${rows}
    Log To Console    number of rows:${row_count}

    FOR    ${index}    IN RANGE    1    ${row_count}+1
        ${col_count}=    Get Element Count    xpath=(//div[@id='credentials']//table//tr)[${index}]/td
        IF    ${col_count} == 2
            ${value}=    Get Value    xpath=(//div[@id='credentials']//table//tr)[${index}]/td[2]/input
            ${value}=    Convert To String    ${value}
            ${value}=    Strip String    ${value}
            Append To List    ${table_data}    ${value}
        END
    END

    Log To Console    📋 Extracted Form Table Values: ${table_data}


    ${checked_labels}=    Extract Checked Tree Labels
    Log To Console    📋 Checked Items: ${checked_labels}

    # --- Ensure all table data values are strings before merging ---
    ${safe_table_data}=    Evaluate    [str(x).strip() for x in @{table_data}]    modules=builtins



    

    # --- Combine and save to Excel ---
# --- Combine and save to Excel correctly ---
    ${row_data}=    Create List    @{table_data}    ${checked_labels}
    ${rows_to_add}=    Create List    ${row_data}
    Append Rows To Sheet    ${EXCEL_FILE}    Credentials    ${rows_to_add}

    Log To Console    ✅ Credentials data written to Excel

    Log To Console    ✅ Credentials data written to Excel 'Credentials' sheet (checked only)

