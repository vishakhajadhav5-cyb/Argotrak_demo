*** Settings ***
Library    SeleniumLibrary
Library    ../../libraries/common/ui_function.py

*** Keywords ***
Login To Agrotrak
    [Arguments]    ${url}    ${username}    ${password}
    Log To Console    🔹 Logging into site: ${url}
    ${driver}=    Open Login    ${url}    ${username}    ${password}
    Log To Console    ✅ Browser opened and login (if any) attempted
    Set Suite Variable    ${driver}

