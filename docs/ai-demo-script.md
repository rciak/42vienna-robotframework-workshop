# AI-Assisted Testing Demo Script

**Duration:** ~15 minutes
**When:** 19:15 in the agenda

## Setup

- Have Claude Code (or Copilot) open in a Codespace terminal
- Have the project README open for context

## Demo Flow

### 1. Natural Language to Test (3 min)

**Say:** "Let me show you how AI can help write tests. I'll describe what I want in plain English."

**Prompt to give Claude Code:**

> Write a Robot Framework test that verifies products on SauceDemo can be sorted by name Z-to-A. The test should log in as standard_user, select the Z-A sort option, and verify the first product name starts with a letter later in the alphabet than the last product.

**Expected output:** A complete `.robot` file with Settings, Variables, Test Cases, and Keywords sections.

### 2. Review the Generated Test (3 min)

**Say:** "Now let's review what the AI generated. Does it look correct?"

Walk through:
- Does it import the right resources?
- Are the selectors correct for SauceDemo?
- Does the sorting assertion make sense?
- Are there any issues?

**Key teaching moment:** AI gets the structure right but may use wrong selectors or flawed assertions. The tester must validate.

### 3. Run the Test (2 min)

```bash
uv run robot tests/student_exercises/ai_generated_sort_test.robot
```

If it passes: "Great, but we still need to verify it's actually testing what we intended."

If it fails: "This is normal! Let's debug and fix it together."

### 4. Refine (3 min)

If the test had issues, refine the prompt:

> The sort dropdown on SauceDemo uses the CSS selector `.product_sort_container` and the Z-A option has value `za`. After sorting, verify the first `.inventory_item_name` text is "Test.allTheThings() T-Shirt (Red)" which is alphabetically last.

### 5. Compare with Hand-Written (2 min)

**Say:** "Now compare this AI-generated test with the hand-written product sort test in our test suite."

Open `tests/03_product_tests/product_catalog.robot` and show the `Sort Products By Price Low To High` test.

**Key points:**
- The hand-written test uses resource file keywords (better abstraction)
- The AI test might use raw selectors (less maintainable)
- AI is great for boilerplate, humans are needed for test strategy

### 6. Wrap Up (2 min)

**Key takeaways:**
- AI saves time on repetitive code
- AI doesn't replace test design thinking
- Always run the test — don't trust unexecuted code
- Use AI for the "how", you decide the "what"

## Backup Demo (if AI tools unavailable)

If Claude Code / Copilot aren't available:

1. Show a pre-generated test file
2. Walk through how it was created
3. Run it live
4. Still do the comparison with hand-written tests

## Pre-Generated Test (backup)

Save this as `tests/student_exercises/ai_demo_sort_test.robot` before the workshop:

```robotframework
*** Settings ***
Documentation     AI-generated test: Verify Z-A product sorting on SauceDemo.
Library           Browser
Resource          ../../resources/common.resource
Resource          ../../resources/login_page.resource
Resource          ../../resources/products_page.resource

Suite Setup       Open SauceDemo
Suite Teardown    Close SauceDemo

*** Test Cases ***
Products Should Sort By Name Z To A
    [Documentation]    Verify that selecting Z-A sort orders products correctly.
    [Tags]    student    exercise    ai-generated
    Login With Credentials    ${VALID_USER}    ${VALID_PASSWORD}
    Login Should Succeed
    Sort Products By    Name (Z to A)
    ${first_product}=    Get Text    css=.inventory_item_name >> nth=0
    Should Be Equal    ${first_product}    Test.allTheThings() T-Shirt (Red)
```
