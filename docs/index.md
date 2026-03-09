# Robot Framework E2E Testing Workshop — 42 Vienna

[![Robot Framework Tests](https://github.com/HackXIt/42vienna-robotframework-workshop/actions/workflows/robot-tests.yml/badge.svg)](https://github.com/HackXIt/42vienna-robotframework-workshop/actions/workflows/robot-tests.yml)

**Browser Library & Playwright for Web Testing**

Workshop Date: March 16, 2026, 16:00 — 42 Vienna, Muthgasse 24-26, 1190 Vienna

## Quick Start (3 steps)

1. **Fork** this repository (click "Fork" on GitHub)
2. **Open a Codespace** on your fork: Code → Codespaces → Create codespace on main
3. **Run the first test:**
   ```bash
   uv run robot tests/00_setup_verification/
   ```

That's it! If the test passes, your environment is ready.

## What is Robot Framework?

Robot Framework is a **generic** test automation framework. Unlike specialized tools (Cypress for web only, Postman for API only), Robot Framework uses **one syntax** and **one reporting format** across different testing domains:

- **Web testing** → Browser Library (Playwright) or SeleniumLibrary
- **API testing** → RequestsLibrary or RESTinstance
- **Mobile testing** → AppiumLibrary
- **Desktop testing** → Various libraries

This workshop focuses on **web testing** using Browser Library against [SauceDemo](https://www.saucedemo.com).

## Prerequisites

- A **GitHub account** (that's it — we use Codespaces)
- Optionally: local setup with Python 3.12+, Node.js 22+, and uv

## Workshop Agenda

1. Welcome, intro, environment setup
2. RF syntax walkthrough + Browser Library basics
3. Guided exercises: Login & Product tests
4. Resource files, keyword abstraction, free exercises
5. AI-assisted testing demo
6. PR creation, CI results, wrap-up

## Documentation

- [Getting Started](getting-started.md) — setup guide (Codespaces, local, Windows)
- [RF Syntax Cheatsheet](rf-syntax-cheatsheet.md) — quick reference
- [Browser Library Guide](browser-library-guide.md) — Browser Library keywords
- [Exercises](exercises.md) — progressive hands-on exercises
- [Optional Practice Sites](optional-practice-sites.md) — additional sites beyond SauceDemo
- [Troubleshooting](troubleshooting.md) — common issues and fixes
- [AI-Assisted Testing](ai-assisted-testing.md) — using AI for test generation
- [Student Workflow](student-workflow.md) — fork, write tests, submit PR
- [Windows Setup](windows-setup.md) — detailed Windows instructions
- [Keyword Documentation](keywords/index.md) — auto-generated keyword reference (libdoc HTML)

## Common Commands

```bash
# Verify environment
python scripts/check_environment.py

# Install dependencies
uv sync

# Initialize browsers
uv run rfbrowser init chromium

# Run all tests
uv run robot tests/

# Run specific suite
uv run robot tests/02_login_tests/

# Run your exercises
uv run robot tests/student_exercises/yourname_*.robot
```

## License

[MIT](https://github.com/HackXIt/42vienna-robotframework-workshop/blob/main/LICENSE) — Nikolaus Rieder, 2026
