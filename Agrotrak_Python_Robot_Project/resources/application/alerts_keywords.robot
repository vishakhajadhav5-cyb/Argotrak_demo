*** Settings ***
Library          SeleniumLibrary
Library          BuiltIn
Library          Collections
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py
Library          OperatingSystem
Library    String
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py

*** Variables ***
${ALERT_TABLE}          //table[@id='alertTable']

*** Keywords ***
Open Alerts Tab
    Log To Console    🔹 Opening Alerts tab...
    Wait Until Element Is Visible    xpath=//button[text()='Alerts']    5s
    Click Element    xpath=//button[text()='Alerts']
    Sleep    1s
    Log To Console    ✅ Alerts tab opened

Process Alerts Table
    [Arguments]    ${excel_file}
    Log To Console    🔹 Checking if Alerts table has rows...
    ${rows_present}=    Run Keyword And Return Status    Page Should Contain Element    ${ALERT_TABLE}//tbody/tr
    Run Keyword If    ${rows_present}    Extract And Save Alerts    ${excel_file}
    Run Keyword If    not ${rows_present}    Log To Console    ⚠️ No rows found in Alerts table


Extract And Save Alerts
    [Arguments]    ${excel_file}
    Log To Console    🔹 Extracting alerts from table...

    ${rows}=    Get WebElements    xpath=//table[@id='alertTable']//tbody/tr
    ${num_rows}=    Get Length    ${rows}
    Log To Console    ℹ️ Found ${num_rows} rows in Alerts table

    FOR    ${i}    IN RANGE    1    ${num_rows + 1}
        ${td_elements}=    Get WebElements    xpath=//table[@id='alertTable']//tbody/tr[${i}]/td
        ${cells}=    Create List

        FOR    ${td}    IN    @{td_elements}
            ${text}=    Get Text    ${td}
            ${text}=    Strip String    ${text}
            Append To List    ${cells}    ${text}
        END

        Log To Console    🔸 Row ${i} values -> ${cells}

        ${has_star}=    Set Variable    False
        ${has_admin}=   Set Variable    False

        FOR    ${value}    IN    @{cells}
            ${value_clean}=    Strip String    ${value}
            ${value_lower}=    Convert To Lowercase    ${value_clean}
            Log To Console    Comparing: [${value_clean}]

            IF    '${value_clean}' == '⭐'
                ${has_star}=    Set Variable    True
            END
            IF    'administrator' in '${value_lower}'
                ${has_admin}=    Set Variable    True
            END
        END

        IF    ${has_star} and ${has_admin}
            Log To Console    ✅ Row ${i} contains ⭐ and Administrator -> ${cells}
            ${group_name}=    Set Variable    ${cells[2]}
            Log To Console    group name -> ${group_name}
            ${arrow_xpath}=    Set Variable    //table[@id='alertTable']//tbody/tr[${i}]/td[2]/button
            Log To Console    🔹 Clicking forward arrow for row ${i}...
            Sleep    1s
            Click Element    ${arrow_xpath}
            Sleep    5s
            Wait Until Element Is Visible    xpath=//div[@id='userSelectorPopup' and contains(@style,'display: block')]    timeout=5s
            Log To Console    ✅ User Selector popup is visible!
            Extract User Popup Data    ${group_name}    ${excel_file}
            BREAK
        END
    END    # ✅ Properly close the FOR loop here

    Sleep    2s
    ${close_popup}=    Set Variable    //*[@id="userSelectorPopup"]/div/button
    Click Element    ${close_popup}
    Sleep    2s




Extract User Popup Data
    [Arguments]    ${group_name}    ${excel_file}
    Wait Until Element Is Visible    id=userSelectorPopup    timeout=5s
    Log To Console    🔍 Extracting values from User Selector popup...

    ${selected_alert}=    Get Text    xpath=//span[@id='selectedAlertName']
    ${copy_alert}=    Get Element Attribute    xpath=//td[normalize-space(text())='Copy Alert:']/following-sibling::td//input    value
    ${ignore_duplicates}=    Get Element Attribute    xpath=//td[normalize-space(text())='Ignore Duplicates Value:']/following-sibling::td//input    value
    ${threshold}=    Get Element Attribute    xpath=//td[normalize-space(text())='Threshold Value:']/following-sibling::td//input    value
    ${start_time}=    Get Element Attribute    xpath=//td[normalize-space(text())='Start Time:']/following-sibling::td//input    value
    ${end_time}=    Get Element Attribute    xpath=//td[normalize-space(text())='End Time:']/following-sibling::td//input    value
    ${email}=    Get Element Attribute    xpath=//td[normalize-space(text())='Delivery Email Address:']/following-sibling::td//input    value
    ${delivery_type}=    Get Element Attribute    xpath=//td[normalize-space(text())='Delivery Type:']/following-sibling::td//input    value

    @{checked_days}=    Get WebElements    xpath=//div[h4[contains(.,'Scheduled Days')]]//label[input[@checked]]
    ${days}=    Create List
    FOR    ${label}    IN    @{checked_days}
        ${day}=    Get Text    ${label}
        Append To List    ${days}    ${day}
    END
    ${days_str}=    Catenate    SEPARATOR=,    @{days}

    Log To Console    ✅ Popup Data:
    Log To Console    Selected Alert: ${selected_alert}
    Log To Console    Copy Alert: ${copy_alert}
    ${cleaned_copy_alert}=    Replace String   ${copy_alert}     *    ${EMPTY}    count=1
    Log To Console    Copy Alert: ${cleaned_copy_alert}
    Log To Console    Ignore Duplicates: ${ignore_duplicates}
    Log To Console    Threshold: ${threshold}
    Log To Console    Scheduled Days: ${days_str}
    Log To Console    Start Time: ${start_time}
    Log To Console    End Time: ${end_time}
    Log To Console    Email: ${email}
    Log To Console    Delivery Type: ${delivery_type}

    ${row}=    Create List    ${group_name}    ${cleaned_copy_alert}    ${ignore_duplicates}    ${threshold}    ${days_str}    ${start_time}    ${end_time}    ${email}    
    ${rows}=    Create List    ${row}
    Log To Console    ✅ Appending row to Excel: ${row}
    Append Rows To Sheet    ${EXCEL_FILE}    Alerts    ${rows}
    Log To Console    ✅ Added popup data to Excel successfully!

