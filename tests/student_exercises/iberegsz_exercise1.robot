*** Settings ***
Documentation     Iberegsz - Exercise 1: Verify valid login for standard_user
Library           Browser
Resource          ../../resources/common.resource
Resource          ../../resources/login_page.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Test Cases ***
Valid Login With Standard User
    [Documentation]    Verify that ${VALID_USER} can log in successfully and reach the products page
    [Tags]    student    exercise
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Login Should Succeed
    # Return to login page so other tests (if added) start from same state
    Go To    ${BASE_URL}

Login With Invalid Password Should Fail
    [Documentation]    Verify that wrong password shows an error message for ${VALID_USER}
    [Tags]    student    exercise
    Login With Credentials    ${VALID_USER}    wrong_password
    Login Should Fail With Message    Username and password do not match
    Go To    ${BASE_URL}
