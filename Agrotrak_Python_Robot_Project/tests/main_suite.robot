*** Settings ***
Documentation     🚜 AgroTrak – Full Automation Suite (With File Logging & Exception Handling)
Resource          ../resources/common/common_keywords.robot
Resource          ../resources/application/devicelist_keywords.robot
Resource          ../resources/application/alerts_keywords.robot
Resource          ../resources/application/reports_keywords.robot
Resource          ../resources/application/maintenance_keywords.robot
Resource          ../resources/application/credential_keywords.robot
Resource          ../resources/common/ui_common.robot

Library           SeleniumLibrary
Library           OperatingSystem
Library           Collections
Library           BuiltIn
Library           Process
Library           ../libraries/common/excel_operation.py
Library           ../libraries/common/config_loader.py
Library           ../libraries/common/logger_library.py

Suite Setup       Initialize Suite
Suite Teardown    Close All Browsers


*** Variables ***
${EXCEL_FILE}        results/output.xlsx
${username}          abcd
${password}          abcd
${PROJECT_ROOT}      ${CURDIR}/..
${DEV_CONFIG}        ${PROJECT_ROOT}/config/dev_config.json
${USER_CONFIG}       ${PROJECT_ROOT}/config/user_config.json
${LOG_FILE}          ${PROJECT_ROOT}/logs/agrotrak_run.log


*** Keywords ***
Initialize Suite
    [Documentation]    Initialize logger, load configurations, and start the automation suite.
    Log To Console     🚀 Initializing AgroTrak Automation Suite...
    Initialize Logger    ${LOG_FILE}
    Log Info    ===== AgroTrak Automation Suite Started =====


Call Multiple UI Functions
    [Arguments]    ${EXCEL_FILE}    ${driver}
    [Documentation]    Executes all UI functional flows with exception handling and logging.

    TRY

        Log Info    📋 Executing: Device List Actions
        Perform Device List Actions
        Sleep    1s

        Log Info    📋 Executing: Alerts Tab Actions
        Open Alerts Tab
        Process Alerts Table    ${EXCEL_FILE}
        Sleep    1s

        Log Info    📋 Executing: Reports Tab Actions
        Open Reports Tab
        Process Reports Tab    ${EXCEL_FILE}
        Sleep    1s

        Log Info    📋 Executing: Maintenance Manager Actions
        Open Tools And Settings
        Open Maintenance Manager    ${EXCEL_FILE}
        Sleep    1s

        Log Info    📋 Executing: Credentials Manager Actions
        Open Tools And Settings Credentials
        Open Manage User Group Access    ${EXCEL_FILE}
        Extract Credentials Data    ${EXCEL_FILE}    ${driver}
        Sleep    1s

        Log Info    ✅ All UI actions completed successfully.

    EXCEPT    AS    ${error}
        Log Error    ❌ Exception occurred during Call Multiple UI Functions: ${error}
        Capture Page Screenshot
        Log To Console    🔥 Exception captured during Call Multiple UI Functions: ${error}
        Append Error To Excel    ${EXCEL_FILE}    CallMultipleUI    ${error}
    FINALLY
        Log Info    🧹 Completed Call Multiple UI Functions (Cleanup Phase)
    END


*** Test Cases ***
Run Multiple Environments
    [Documentation]    Loads configurations, executes full end-to-end AgroTrak + NewGate workflow.

    TRY
        Log Info    🚀 Loading Environment Configurations
        ${envs}=    Load All Config    ${DEV_CONFIG}    ${USER_CONFIG}
        Log Info    ✅ Configurations Loaded Successfully

        Log Info    🌍 AgroTrak URL: ${envs['argotrak']['argotrak_url']}
        Log Info    👤 AgroTrak Username: ${envs['argotrak']['argotrak_username']}
        Log Info    🌍 NewGate URL: ${envs['newgate']['newgate_url']}

        Log Info    📊 Initializing Excel setup
        Setup Excel    ${EXCEL_FILE}

        # --- AgroTrak ---
        Log Info    🌍 Logging into AgroTrak
        ${status}=    Run Keyword And Return Status    Login To Agrotrak
        ...    ${envs['argotrak']['argotrak_url']}
        ...    ${envs['argotrak']['argotrak_username']}
        ...    ${envs['argotrak']['argotrak_password']}

        Run Keyword If    not ${status}    Log Error    ❌ AgroTrak login failed!
        Run Keyword If    ${status}         Log Info    ✅ AgroTrak login successful.

        Call Multiple UI Functions    ${EXCEL_FILE}    ${driver}

        # --- NewGate ---
        Log Info    🌍 Logging into NewGate
        ${status2}=    Run Keyword And Return Status    Login To Agrotrak
        ...    ${envs['newgate']['newgate_url']}
        ...    ${envs['newgate']['newgate_username']}
        ...    ${envs['newgate']['newgate_password']}

        Run Keyword If    not ${status2}    Log Error    ❌ NewGate login failed!
        Run Keyword If    ${status2}        Log Info    ✅ NewGate login successful.

        Log Info    ===== Test Suite Completed Successfully =====

    EXCEPT    AS    ${error}
        Log Error    ❌ Exception caught during Run Multiple Environments: ${error}
        Capture Page Screenshot
        Append Error To Excel    ${EXCEL_FILE}    RunMultipleEnv    ${error}
        Log To Console    🚨 Exception: ${error}

    FINALLY
        Log Info    🧹 Cleaning up and closing browsers
        Close All Browsers
        Log Info    ===== Suite Execution Ended =====
    END

