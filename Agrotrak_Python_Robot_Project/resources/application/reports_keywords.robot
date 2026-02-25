*** Settings ***
Library          SeleniumLibrary
Library          BuiltIn
Library          Collections
Library          OperatingSystem
Library          String
Library          C:/Users/vishakhajad/Desktop/ArgoTrak_Project/Agrotrak_Python_Robot_Project/libraries/common/excel_operation.py


*** Variables ***
${REPORT_CARD}          css:div.report-card
${SCHEDULER_POPUP}     id=schedulerPopup
${SCHEDULER_INPUTS}    xpath=//*[@id="schedulerPopup"]//input
${SCHEDULER_CLOSE}     xpath=//*[@id="schedulerPopup"]//button[contains(text(),'Close')]

*** Keywords ***
Open Reports Tab
    Log To Console    🔹 Opening Reports tab...
    Wait Until Element Is Visible    xpath=//button[normalize-space()='Reports']    5s
    Click Element    xpath=//button[normalize-space()='Reports']
    Sleep    1s
    Log To Console    ✅ Reports tab opened successfully


Process Reports Tab
    [Arguments]    ${excel_file}
    Log To Console    🔍 Scanning Reports cards for Scheduled entries...
    ${report_cards}=    Get WebElements    ${REPORT_CARD}

    Run Keyword If    '${report_cards}' == '[]'    Log To Console    ⚠️ No report cards found!    AND    RETURN

    FOR    ${card}    IN    @{report_cards}
        ${text}=    Get Text    ${card}
        ${text_lower}=    Convert To Lowercase    ${text}
        Log To Console    🪶 Checking card text: ${text_lower}

        ${contains}=    Run Keyword And Return Status    Should Contain    ${text_lower}    scheduled

        IF    ${contains}
            Log To Console    ✅ YES – this card contains 'scheduled'
            Click Element    xpath=//*[@id="reports"]/div/div/button
            Sleep    5s
            Wait Until Element Is Visible    ${SCHEDULER_POPUP}    5s
            Extract Scheduler Popup Data    ${excel_file}
            Exit For Loop
        ELSE
            Log To Console    ❌ NO – this card does not contain 'scheduled'
        END
    END


Extract Scheduler Popup Data
    [Arguments]    ${excel_file}
    Log To Console    🧠 Extracting scheduler popup data...
    ${inputs}=    Get WebElements    ${SCHEDULER_INPUTS}
    ${row_data}=    Create List

    FOR    ${inp}    IN    @{inputs}
        ${val}=    Get Element Attribute    ${inp}    value
        ${val}=    Strip String    ${val}
        Append To List    ${row_data}    ${val}
    END

    Log To Console    📋 Extracted Report Scheduler Data:
    FOR    ${item}    IN    @{row_data}
        Log To Console    → ${item}
    END

    # ✅ Append extracted data to Excel
    ${rows}=    Create List    ${row_data}
    Append Rows To Sheet    ${excel_file}    Reports    ${rows}
    Log To Console    ✅ Data written successfully to Excel 'Reports' sheet.

    # ✅ Close the popup
    Click Element    ${SCHEDULER_CLOSE}
    Log To Console    ✅ Scheduler popup closed successfully.

