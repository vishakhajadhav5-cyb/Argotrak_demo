*** Settings ***
Library          SeleniumLibrary
Library          Collections
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/application/devicelist_table.py
# Resource         C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/resources/common/excel_operations.robot
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py

*** Keywords ***
Perform Device List Actions
    [Documentation]    Perform all actions for Main Device List tab
    Log To Console    🧭 Performing Main Device List actions...
    Wait Until Element Is Visible    xpath=//button[contains(text(),'Main Device List')]    5s
    Click Element    xpath=//button[contains(text(),'Main Device List')]
    Sleep    1s
    Log To Console    ✅ Clicked Main Device List Tab

    # Click the Download button if visible
    ${is_download_visible}=    Run Keyword And Return Status
    ...    Element Should Be Visible    xpath=//button[contains(text(),'Download') or contains(@id,'download')]
    Run Keyword If    ${is_download_visible}    Click Element    xpath=//button[contains(text(),'Download') or contains(@id,'download')]
    Run Keyword If    ${is_download_visible}    Log To Console    ✅ Download Button Clicked
    ...    ELSE    Log To Console    ⚠️ Download Button not found.

    # Extract table data if it exists
    ${table_present}=    Run Keyword And Return Status    Page Should Contain Element    xpath=//table[@id='deviceTable']
    Run Keyword If    ${table_present}    Extract And Save Device Table
    ...    ELSE    Log To Console    ⚠️ No device table found on the page.



Extract And Save Device Table
    [Documentation]    Extract device list table and append to Excel
    ${rows}=    Extract Device Table
    Log To Console    🖨️ Extracted rows:
    FOR    ${row}    IN    @{rows}
        Log To Console    ${row}
    END
    Append Rows To Sheet    ${EXCEL_FILE}    MainDeviceList    ${rows}

