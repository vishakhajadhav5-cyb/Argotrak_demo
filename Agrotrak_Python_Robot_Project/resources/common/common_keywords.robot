*** Settings ***
Library    SeleniumLibrary
Library    JSONLibrary
Library    OperatingSystem
Library    Collections

*** Variables ***
${CONFIG_FILE}    ${CURDIR}/../../config/config.json

*** Keywords ***
Load Config
    Log To Console    🌐 Loading configuration file...
    ${config}=    Load JSON From File    ${CONFIG_FILE}

    # ✅ Load main site URL
    ${SITE_URL}=    Get Value From Json    ${config}    $.site_url
    ${SITE_URL}=    Set Variable    ${SITE_URL[0]}

    # ✅ Load dummy site URLs (dictionary)
    ${dummy_site_urls}=    Get Value From Json    ${config}    $.dummy_site_urls
    ${dummy_site_urls}=    Set Variable    ${dummy_site_urls[0]}

    # ✅ (Optional) Load credentials if added later in config
    ${username}=    Run Keyword And Ignore Error    Get Value From Json    ${config}    $.username
    ${password}=    Run Keyword And Ignore Error    Get Value From Json    ${config}    $.password

    # ✅ Set them as suite-level variables for all tests
    Set Suite Variable    ${SITE_URL}
    Set Suite Variable    ${dummy_site_urls}
    Set Suite Variable    ${username}
    Set Suite Variable    ${password}

    # ✅ Confirmation logs
    Log To Console    🌐 Loaded Site URL: ${SITE_URL}
    Log To Console    🧠 Loaded Dummy URLs: ${dummy_site_urls}
    Log To Console    🔐 Username: ${username}
    Log To Console    ✅ Configuration loaded successfully!


