# Workshop Agenda — Instructor Notes

**Date:** March 16, 2026, 16:00
**Duration:** ~4 hours
**Location:** 42 Vienna, Muthgasse 24-26, 1190 Vienna

## Agenda

| Activity | Details |
|----------|---------|
| Welcome & Setup | Intro, fork repo, open Codespace, run `check_environment.py` |
| Robot Framework Overview | What is RF, why generic > specialized, comparison with Cypress/Postman |
| RF Syntax Walkthrough | Live coding with cheat sheet, variables, keywords, sections |
| Browser Library Demo | Run `first_browser_test.robot`, explain selectors, auto-wait |
| **Break** | |
| Exercise: Login Tests (Ex 2-3) | Students write tests, instructor walks around |
| Exercise: Products & Cart (Ex 4) | More independence, less guidance |
| **Break** | |
| Resource Files & Keyword Abstraction | Show page object pattern, import chain |
| Free Exercise: E2E Scenario (Ex 5-6) | Independent or pair work |
| AI-Assisted Testing Demo | Claude Code generates test from natural language |
| PR Submission & CI Results | Students create PRs, review CI feedback |
| Wrap-up & Q&A | RF ecosystem, next steps, feedback |

## Key Talking Points

### Why Robot Framework?

- **Generic framework:** One syntax, one reporting format, swap libraries for different domains
  - Web → Browser Library (Playwright) or SeleniumLibrary
  - API → RequestsLibrary or RESTinstance
  - Mobile → AppiumLibrary
  - Desktop → Various libraries
- **Contrast with specialized tools:** Cypress/Playwright/Puppeteer for web only, Postman for API only, Appium standalone for mobile — each has different syntax, reporting, CI setup
- **Keyword-driven:** Non-programmers can read and understand tests
- **Built-in reporting:** HTML reports with screenshots, timing, and pass/fail without any extra setup

### Browser Library vs SeleniumLibrary

- Browser Library uses Playwright → faster, more reliable, built-in auto-waiting
- SeleniumLibrary uses Selenium WebDriver → older, more browser support, larger community
- This workshop uses Browser Library (modern choice)

### AI + Testing

- AI doesn't replace testers — it accelerates test creation
- Tester designs strategy and validates results; AI generates boilerplate
- Demo: describe test in English → AI generates `.robot` file → run → refine

## Setup Phase (16:00-16:15)

### Before students arrive

1. Open the repo in a browser tab: https://github.com/HackXIt/42vienna-robotframework-workshop
2. Have a Codespace ready as demo environment
3. Verify SauceDemo is up: https://www.saucedemo.com

### Student setup steps

Guide students through:

1. **Fork** the repo (show on projector)
2. **Create Codespace** on their fork
3. Wait for build (~3-5 min)
4. Run verification: `uv run robot tests/00_setup_verification/`

### If a student has issues

- Run `python scripts/check_environment.py` for diagnostics
- Common fix: `uv run rfbrowser init chromium` (browser not initialized)
- Last resort: pair with another student

## Fallback Plan: SauceDemo Down

If https://www.saucedemo.com is unavailable:

1. **Check status** — try from mobile hotspot (might be network-specific)
2. **Alternative SUT:** https://the-internet.herokuapp.com
   - Simpler but covers login, forms, dynamic content
   - Would need to modify resource files (selectors)
3. **Offline option:** Use RF with non-browser libraries for the syntax portion
   - `BuiltIn` library exercises (string manipulation, list operations)
   - Teach RF syntax without SauceDemo dependency

## Adding Collaborators (Plan B)

If forking causes friction, add students as collaborators:

```bash
# Replace USERNAME with student's GitHub username
gh api repos/HackXIt/42vienna-robotframework-workshop/collaborators/USERNAME --method PUT --field permission=push
```

Students then clone directly (no fork) and work on branches.

## Post-Workshop

- Review and merge student PRs
- Collect feedback (what worked, what was confusing)
- Share resources: RF docs, Browser Library docs, this repo
