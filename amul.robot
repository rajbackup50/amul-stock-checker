*** Settings ***
Library    Browser
Library    Dialogs
Suite Teardown    Close Browser    ALL

*** Variables ***
@{products_to_be_searched}
...    Amul High Protein Buttermilk, 200 mL | Pack of 30
...    Amul High Protein Rose Lassi, 200 mL | Pack of 30
...    Amul High Protein Blueberry Shake, 200 mL | Pack of 30

*** Test Cases ***
Verify if amul product is available or not
    New Browser    chromium    headless=True
    New Page       https://shop.amul.com/en/

    # Enter the pincode to check delivery availability
    Fill Text    xpath=//input[@placeholder="Enter Your Pincode"]    400701
    Wait For Elements State    xpath=//p[text()="400701"]    visible
    Click        xpath=//div[normalize-space()="400701"]

    FOR    ${product}    IN    @{products_to_be_searched}
        Log To Console    \n🔍 Checking availability for: ${product}
        Click    xpath=//input[@id="searchtext"]
        Type Text    xpath=//input[@id="searchtext"]    ${product}
        Press Keys    xpath=//input[@id="searchtext"]    Enter
        Click    xpath=//a[text()="${product}"]
        Get Text    .product-name   contains    ${product}
        ${sold_out_status}=    Run Keyword And Return Status    Get Text    .alert-danger    ==   Sold Out
        IF    ${sold_out_status}
            Log To Console    \n❌ Broke my heart, the product is sold out: ${product}
        ELSE
            Log To Console    \n✅ Yay! ${product} is available for purchase
        END
        Go To    https://shop.amul.com/en/
    END
