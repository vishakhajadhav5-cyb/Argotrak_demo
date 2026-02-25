*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem
Library    BuiltIn
Library    ../../libraries/common/logger_library.py
Library    ../../libraries/common/excel_operation.py

*** Variables ***
${LOG_DIR}          ${EXECDIR}/logs
${SCREENSHOT_DIR}   ${EXECDIR}/logs/screenshots
${RESULT_FILE}      ${EXECDIR}/results/output.xlsx

*** Keywords ***
Handle Exception
    [Arguments]    ${error_message}    ${screenshot_name}=error_screenshot    ${module}=General
    Log To Console    ❌ Exception caught: ${error_message}
    Log To App Logger    ERROR    Exception caught in ${module}: ${error_message}

    # Ensure directories exist
    Run Keyword And Ignore Error    Create Directory    ${LOG_DIR}
    Run Keyword And Ignore Error    Create Directory    ${SCREENSHOT_DIR}
    Run Keyword And Ignore Error    Create Directory    ${EXECDIR}/results

    ${ts}=    Get Time    format=%Y%m%d_%H%M%S
    ${screenshot_path}=    Set Variable    ${SCREENSHOT_DIR}/${screenshot_name}_${ts}.png
    Run Keyword And Ignore Error    Capture Page Screenshot    ${screenshot_path}
    Log To App Logger    INFO    Screenshot saved: ${screenshot_path}
    Log To Console    📸 Screenshot: ${screenshot_path}

    # Write a result row to Excel (non-blocking)
    Run Keyword And Ignore Error    Setup Excel    ${RESULT_FILE}
    ${message}=    Catenate    SEPARATOR= |    ${error_message}    Screenshot=${screenshot_path}
    Run Keyword And Ignore Error    Append Result Row    ${RESULT_FILE}    ${module}    FAILED    ${message}

    # Fail current test gracefully with message
    Fail    ${error_message}
