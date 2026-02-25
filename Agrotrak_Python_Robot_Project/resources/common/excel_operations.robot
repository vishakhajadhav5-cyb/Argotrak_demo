*** Settings ***
Library    RPA.Excel.Files
Library    OperatingSystem
Library    Collections
Library    String    # ✅ Added this line!

*** Variables ***
${EXCEL_FILE}    results/output/output.xlsx

*** Keywords ***
Ensure Excel And Sheets Exist
    [Documentation]    Create Excel if not exists and ensure all required sheets with headers.

    ${file_exists}=    Run Keyword And Return Status    File Should Exist    ${EXCEL_FILE}
    IF    not ${file_exists}
        Create Excel File
    END

    Open Workbook    ${EXCEL_FILE}
    @{sheets}=    Get Worksheet Names

    &{required_sheets}=    Create Dictionary
    ...    MainDeviceList=Status,Last Message Date,Client Name,Device Name,IMEI,SMS Number,Last Reported Date,Modified By,Modified,VIN,Group Name,Created Date,Hardware Name,IP Address
    ...    Alerts=Group Name,Alert Name,Ignore Duplicates Alerts within minutes,Threshold /Value (nmi),Scheduled Days,Start Time,End Time,Delivery action email/sms
    ...    Reports=Report Name,Email to,Email subject,Report Language,Report File format,Send time,Repeat Frequency,Start Date
    ...    Maintenance=Operation,Description
    ...    Credentials=Full Name,Username,Associated Group Name,Group Filter,Associate Items
    ...    Results=Timestamp,Module Name,Status,Message

    FOR    ${sheet_name}    ${headers}    IN    &{required_sheets}
        IF    '${sheet_name}' not in @{sheets}
            Add Worksheet    ${sheet_name}
        END
        ${current_headers}=    Read Row    1    worksheet=${sheet_name}
        IF    len(${current_headers}) == 0
            Write Row    1    ${headers.split(',')}    worksheet=${sheet_name}
        END
    END

    Save Workbook
    Close Workbook


Create Excel File
    [Documentation]    Create output Excel file and folders if missing.
    ${dir}=    Normalize Path    ${EXCEL_FILE}
    ${parent_dir}=    Replace String Using Regexp    ${dir}    (.*)[/\\\\][^/\\\\]+$    \1
    Create Directory    ${parent_dir}
    Create File    ${EXCEL_FILE}


