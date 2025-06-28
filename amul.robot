*** Settings ***
Library    Browser
Library    Dialogs
Suite Teardown    Close Browser    ALL

*** Variables **
${product_to_be_searched}    Amul High Protein Buttermilk, 200 mL | Pack of 30


*** Test Cases ***
Verify if amul product is available or not
    # Open a new Chromium browser (not headless)
    New Browser    chromium    headless=True

    # Set browser window size

    # Open the Amul online shop homepage
    New Page       https://shop.amul.com/en/

    # Enter the pincode to check delivery availability
    fill Text    xpath=//input[@placeholder="Enter Your Pincode"]    400701

    # Wait until the entered pincode is visible in the dropdown
    Wait For Elements State    xpath=//p[text()="400701"]    visible

    # Select the pincode from the dropdown
    Click        xpath=//div[normalize-space()="400701"]

    # Click on the search box
    Click    xpath=//input[@id="searchtext"]

    # Type the product name to search
    Type Text    xpath=//input[@id="searchtext"]    ${product_to_be_searched}

    # Press Enter to search for the product
    Press Keys    xpath=//input[@id="searchtext"]    Enter

    # Click on the searched product from the results
    Click    xpath=//a[text()="${product_to_be_searched}"]

    # Verify the product name is displayed on the product page
    Get Text    .product-name   contains    ${product_to_be_searched}

    # Check if the product is sold out
    ${sold_out_status}=    Run Keyword And Return Status    Get Text    .alert-danger    ==   Sold Out

    # Print result to console based on product availability
    IF    ${sold_out_status}
        Log To Console    \nBroke my heart, the product is sold out
    ELSE
        Log To Console    \nYay! The product is available for purchase
    END

