# Robot Framework Syntax Cheatsheet

## File Structure

Every `.robot` file can have up to four sections:

```robotframework
*** Settings ***     # Imports, suite config
*** Variables ***    # Reusable values
*** Test Cases ***   # The actual tests
*** Keywords ***     # Custom reusable steps (like functions)
```

## Settings Section

```robotframework
*** Settings ***
Documentation     Description of this test suite
Library           Browser                          # Import a test library
Resource          ../resources/common.resource     # Import a resource file
Suite Setup       Open SauceDemo                   # Run before all tests
Suite Teardown    Close SauceDemo                  # Run after all tests
Test Setup        Go To    ${BASE_URL}             # Run before each test
Test Teardown     Take Screenshot                  # Run after each test
```

## Variables

```robotframework
*** Variables ***
${SCALAR}       single value              # Scalar variable
${URL}          https://www.example.com
${NUMBER}       ${42}                     # Number (note the ${} syntax)
${TRUE_VAL}     ${True}                   # Boolean
@{LIST}         item1    item2    item3   # List variable
&{DICT}         key1=val1    key2=val2    # Dictionary variable
${EMPTY}                                  # Built-in: empty string
```

**Using variables:**
```robotframework
Log    ${SCALAR}           # Use in keywords
Log    ${LIST}[0]          # List indexing
Log    ${DICT}[key1]       # Dict access
```

## Test Cases

```robotframework
*** Test Cases ***
My First Test
    [Documentation]    What this test verifies
    [Tags]    smoke    login
    Keyword One    arg1    arg2
    ${result}=    Keyword That Returns    arg1
    Should Be Equal    ${result}    expected_value
```

**Important:** Arguments are separated by **2+ spaces** (or a tab). This is how RF distinguishes keyword names from arguments.

```
Keyword Name    argument1    argument2
^^^ keyword ^^^ ^^^ arg1 ^^^ ^^^ arg2 ^^^
```

## Keywords (like functions)

```robotframework
*** Keywords ***
Login As Standard User
    [Documentation]    Log in with the standard test user
    Fill Text    id=user-name    standard_user
    Fill Text    id=password     secret_sauce
    Click        id=login-button

Login With Credentials
    [Arguments]    ${username}    ${password}
    Fill Text    id=user-name    ${username}
    Fill Text    id=password     ${password}
    Click        id=login-button

Get Product Count
    [Documentation]    Returns the number of products on the page
    ${items}=    Get Elements    css=.inventory_item
    ${count}=    Get Length    ${items}
    RETURN    ${count}
```

## Control Flow (comparison with C)

| C | Robot Framework |
|---|----------------|
| `if (x == 1)` | `IF    $x == 1` |
| `else if` | `ELSE IF    $x == 2` |
| `else` | `ELSE` |
| `for (i=0; i<n; i++)` | `FOR    ${i}    IN RANGE    ${n}` |
| `for (item in list)` | `FOR    ${item}    IN    @{LIST}` |

```robotframework
# IF/ELSE
IF    $count > 0
    Log    Cart has items
ELSE
    Log    Cart is empty
END

# FOR loop
FOR    ${item}    IN    Apple    Banana    Cherry
    Log    ${item}
END

# FOR with RANGE (like C: for i=0; i<5; i++)
FOR    ${i}    IN RANGE    5
    Log    Iteration ${i}
END
```

## Common Built-in Keywords

| Keyword | Example | Purpose |
|---------|---------|---------|
| `Log` | `Log    Hello` | Print to log |
| `Should Be Equal` | `Should Be Equal    ${a}    ${b}` | Assert equality |
| `Should Contain` | `Should Contain    ${text}    hello` | Assert substring |
| `Should Be True` | `Should Be True    ${count} > 0` | Assert condition |
| `Set Variable` | `${x}=    Set Variable    hello` | Assign variable |
| `Sleep` | `Sleep    2s` | Wait (avoid in tests!) |

## Data-Driven Testing with [Template]

```robotframework
*** Test Cases ***
Login Should Fail With Bad Credentials
    [Documentation]    Test multiple invalid login combinations
    [Template]    Verify Login Failure
    # username          password        expected error
    ${EMPTY}            secret_sauce    Username is required
    standard_user       ${EMPTY}        Password is required
    standard_user       wrong           Username and password do not match
    locked_out_user     secret_sauce    this user has been locked out

*** Keywords ***
Verify Login Failure
    [Arguments]    ${username}    ${password}    ${error_message}
    Login With Credentials    ${username}    ${password}
    Login Should Fail With Message    ${error_message}
```
