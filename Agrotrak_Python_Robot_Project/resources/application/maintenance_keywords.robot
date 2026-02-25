*** Settings ***
Documentation    🔧 Maintenance Manager – Handle tools and extract maintenance data
Library          SeleniumLibrary
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py

*** Keywords ***
Open Tools And Settings
    [Documentation]    Click on Settings icon → Tools & Settings link
    Log To Console    🔍 Clicking Settings → Tools & Settings...
    ${is_icon}=    Run Keyword And Return Status    Element Should Be Visible    css:.nav-icon.settings-icon img
    Run Keyword If    ${is_icon}    Click Element    css:.nav-icon.settings-icon img
    Sleep    0.5s
    Run Keyword If    ${is_icon}    Click Element    xpath=//div[@id='settingsDropdown']//a[contains(text(),'Tools & Settings')]
    Sleep    1s
    Log To Console    ✅ Tools & Settings tab opened


Open Maintenance Manager
    [Arguments]    ${EXCEL_FILE}
    [Documentation]    Click “Maintenance Manager” and extract table data
    Log To Console    🔍 Looking for 'Maintenance Manager' button...

    ${status}=    Run Keyword And Return Status    Element Should Be Visible    xpath=//*[@id='toolsSettingsTab']/div/div[1]/ul/li[1]/button
    Run Keyword Unless    ${status}    Log To Console    ⚠️ Maintenance Manager button not found
    Run Keyword Unless    ${status}    RETURN

    Click Element    xpath=//*[@id='toolsSettingsTab']/div/div[1]/ul/li[1]/button
    Sleep    1s

    ${table_visible}=    Run Keyword And Return Status    Wait Until Element Is Visible    xpath=//div[@id='toolsMainContent']//table    timeout=5s
    Run Keyword Unless    ${table_visible}    Log To Console    ⚠️ Maintenance table did not load
    Run Keyword Unless    ${table_visible}    RETURN

    ${rows}=    Get Element Count    xpath=//div[@id='toolsMainContent']//table//tr
    Run Keyword If    ${rows} <= 1    Log To Console    ⚠️ Maintenance table not visible or empty
    Run Keyword If    ${rows} <= 1    RETURN

    # ✅ Add header row if not already present
    # Append Rows To Sheet    ${EXCEL_FILE}    Maintenance    Operation    Description

    Log To Console    📋 Extracted Maintenance Table Data:
    FOR    ${index}    IN RANGE    2    ${rows}+1
        ${cols}=    Get WebElements    xpath=//div[@id='toolsMainContent']//table//tr[${index}]/td
        ${data}=    Create List
        FOR    ${cell}    IN    @{cols}
            ${text}=    Get Text    ${cell}
            ${text}=    Replace String    ${text}    \n    ${SPACE}
            ${text}=    Strip String    ${text}
            Run Keyword If    '${text}' != ''    Append To List    ${data}    ${text}
        END

        ${data_length}=    Get Length    ${data}
        Run Keyword If    ${data_length} > 0    Log To Console    ${data}

        # ✅ Wrap ${data} inside another list to send correctly to Python
        ${row_list}=    Create List    ${data}
        Run Keyword If    ${data_length} > 0    Append Rows To Sheet    ${EXCEL_FILE}    Maintenance    ${row_list}
    END

    Log To Console    ✅ Maintenance data written to Excel sheet

