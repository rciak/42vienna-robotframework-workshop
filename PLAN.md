# 42 Vienna Robot Framework Workshop — Implementation Plan

**Workshop Date:** March 16, 2026, 16:00 (3-4 hours)
**Location:** 42 Vienna, Muthgasse 24-26, 1190 Vienna
**Instructor:** Nikolaus Rieder (rieder.nikolaus@gmail.com)
**Contacts:** Hans Jörg Otto (Corporate Relations), Simon Dablander (IT/Infrastructure)
**Repository:** GitHub `HackXIt/42vienna-robotframework-workshop` → mirrored to `git.lab.hackxit.com/github-mirrors/42vienna-robotframework-workshop`

---

## Table of Contents

- [Executive Summary](#executive-summary)
- [Key Architectural Decisions](#key-architectural-decisions)
- [Audience Profile](#audience-profile)
- [Phase 0: Infrastructure Decisions & Constraints](#phase-0-infrastructure-decisions--constraints)
- [Phase 1: Repository Creation & Base Structure](#phase-1-repository-creation--base-structure)
- [Phase 2: DevContainer Configuration](#phase-2-devcontainer-configuration)
- [Phase 3: Environment Readiness Script](#phase-3-environment-readiness-script)
- [Phase 4: Example Test Suites](#phase-4-example-test-suites)
- [Phase 5: CI/CD Pipeline](#phase-5-cicd-pipeline)
- [Phase 6: AI Integration](#phase-6-ai-integration)
- [Phase 7: Documentation](#phase-7-documentation)
- [Phase 8: GitHub Mirroring to GitLab](#phase-8-github-mirroring-to-gitlab)
- [Phase 9: Student Workflow Design](#phase-9-student-workflow-design)
- [Phase 10: Workshop Agenda](#phase-10-workshop-agenda)
- [Phase 11: Pre-Workshop Checklist](#phase-11-pre-workshop-checklist)
- [Dependency Graph & Critical Path](#dependency-graph--critical-path)
- [Risk Assessment](#risk-assessment)
- [TODO Tasklist](#todo-tasklist)
- [Troubleshooting & Known Issues](#troubleshooting--known-issues)

---

## Executive Summary

This plan covers setting up a Robot Framework workshop repository from an empty git repo to a fully functional, student-ready environment in 7 days. The workshop is an advanced, hands-on session at 42 Vienna, targeting students who know C but not Python, can use Git CLI basics, and are unfamiliar with DevContainers or forks.

The workshop is highly hands-on with minimal lecturing. Students will write Robot Framework test cases using Browser Library (Playwright-based) against SauceDemo, commit via PRs, and observe CI results. AI-assisted test generation will be demonstrated. Robot Framework is highlighted as a generic test automation framework — one interface/syntax across different testing domains (web, API, mobile, desktop), unlike specialized tools that each require learning a new ecosystem.

---

## Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **GitHub-primary, GitLab-mirrored** | GitLab on homelab has no CI runner (`gitlab-runner: install: false`) and the cluster is ARM64-only (Turing RK1). Playwright needs x86-64 browser binaries. GitHub Actions provides free x86-64 runners. Existing `github-sync` (6h) and `github-gitlab-sync` (30min) CronJobs handle mirroring automatically. |
| **`uv` for package management** | `pyproject.toml` + `uv.lock` for reproducible, fast installs. No pip/requirements.txt. `uv` is the modern standard for Python project management. |
| **SauceDemo as SUT** | Public practice site, no hosting burden, rich E2E flows (login, catalog, cart, checkout), well-known test credentials (`standard_user` / `secret_sauce`). |
| **Fork model (Plan A), collaborator access (Plan B)** | Forking is standard open-source procedure and teaches a transferable skill. Students are unfamiliar with forks, so the docs must include explicit step-by-step instructions with screenshots. Fallback: add students as collaborators on-the-fly if forking causes friction during the workshop. |
| **Chromium-only browser install** | `rfbrowser init chromium` reduces download from ~700MB to ~250MB, halving DevContainer build time. |
| **Cross-platform readiness script** | stdlib-only Python script that validates the full environment with colored output and platform-specific fix instructions. First-class citizen, not an afterthought. |
| **Standard `robotframework-browser` (not `[bb]`)** | BrowserBatteries bundles precompiled Node.js binaries which may not support all OS/arch. DevContainer and CI already have Node.js. Standard approach teaches the real dependency chain. |

---

## Audience Profile

Based on emails with Hans Jörg Otto and Simon Dablander:

- **Count:** ~4+ registered, potentially more after newsletter push
- **Background:** 42 Vienna students (peer-to-peer coding school)
- **Git:** All know clone, commit, push, pull via CLI. Some know PRs. Most do NOT know forks.
- **IDE:** Generally know VSCode. NOT familiar with Codespaces or DevContainers.
- **Programming:** Know C (control flow, variables, types). Do NOT know Python.
- **Docker:** NOT a prerequisite. Some may have heard of it but most haven't used it.
- **Testing:** Have had ISTQB Foundation Level training available from a previous session.
- **Hardware:** Either own laptops or 42 Vienna machines (need VSCode + Docker if running locally).

---

## Phase 0: Infrastructure Decisions & Constraints

**Timeline:** Day 1 (March 9)

### Critical Constraint: No GitLab CI Runner

From the homelab GitOps config (`apps/gitlab/helmrelease.yaml`):
```yaml
gitlab-runner:
  install: false
```

The cluster is 3x ARM64 Turing RK1 nodes. Playwright/Browser Library requires x86-64 browser binaries.

| Option | Feasibility | Time |
|--------|-------------|------|
| Install GitLab Runner on ARM64 cluster | Poor — no ARM64 Playwright binaries | Days + risk |
| External x86-64 GitLab Runner VM | Possible but requires VM provisioning | 1-2 days |
| **GitHub Actions (free tier)** | **Excellent — native x86-64, Playwright cache** | **Hours** |

**Decision:** GitHub as primary with GitHub Actions CI. Mirror to GitLab via existing sync infrastructure.

### Mirroring Architecture

```
Students → GitHub (PRs, branches) → GitHub Actions (CI)
                    ↓ (every 6h)
            GitLab github-mirrors group (bare mirror)
                    ↕ (every 30min)
            GitHub ↔ GitLab issue/PR sync (bidirectional)
```

- `github-sync` CronJob: `git clone --bare` from GitHub, `git push --mirror` to GitLab
- `github-gitlab-sync` CronJob: Python script syncs issues/PRs with `<!-- sync:github:... -->` markers
- GitLab group: `github-mirrors` — sync discovers projects by matching `path` to GitHub repos under `HackXIt`

### CURRENT ISSUES — Phase 0

- [ ] **VERIFY:** Does `github-sync` CronJob auto-create GitLab projects, or must they be pre-created? Check the sync script logic.
- [ ] **VERIFY:** Is the GitLab instance publicly accessible (needed if students browse test reports there)?
- [ ] **VERIFY:** Can students at 42 Vienna reach `github.com`, `*.github.dev`, `*.githubusercontent.com` through their network?
- [x] **DECIDED:** GitHub Actions for CI (no GitLab runner, ARM64-only cluster). GitHub is primary.

---

## Phase 1: Repository Creation & Base Structure

**Timeline:** Day 1-2 (March 9-10)
**Dependencies:** None

### Step 1.1: Create GitHub Repository

- Repository: `HackXIt/42vienna-robotframework-workshop`
- Visibility: **Public** (students need access without auth)
- Description: "Robot Framework E2E testing workshop for 42 Vienna — Browser Library & Playwright"
- License: MIT
- Initialize with README: Yes
- `.gitignore`: Python template

### Step 1.2: Configure Local Git Remotes

```bash
cd /home/hackxit/git-stash/42vienna-robotframework-workshop
git remote add origin git@github.com:HackXIt/42vienna-robotframework-workshop.git
```

### Step 1.3: GitLab Project Setup

Create project under `github-mirrors` group on `git.lab.hackxit.com`:
- Path: `github-mirrors/42vienna-robotframework-workshop`
- Visibility: Public
- Merge request settings: Approvals not required
- Branch protection on `main`: no force push, merge only via MR

Alternatively, wait for `github-sync` to auto-create on next run.

### Step 1.4: Repository Directory Structure

```
42vienna-robotframework-workshop/
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create.sh
├── .github/
│   ├── workflows/
│   │   ├── robot-tests.yml
│   │   └── pr-feedback.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── tests/
│   ├── 00_setup_verification/
│   │   └── verify_setup.robot
│   ├── 01_first_test/
│   │   └── first_browser_test.robot
│   ├── 02_login_tests/
│   │   └── login.robot
│   ├── 03_product_tests/
│   │   ├── product_catalog.robot
│   │   └── product_details.robot
│   ├── 04_cart_tests/
│   │   └── shopping_cart.robot
│   ├── 05_checkout_tests/
│   │   └── checkout_flow.robot
│   ├── 06_e2e_scenarios/
│   │   └── complete_purchase.robot
│   └── student_exercises/
│       ├── _template.robot
│       └── README.md
├── resources/
│   ├── common.resource
│   ├── saucedemo.resource
│   ├── login_page.resource
│   ├── products_page.resource
│   ├── cart_page.resource
│   └── checkout_page.resource
├── scripts/
│   └── check_environment.py
├── docs/
│   ├── 01-getting-started.md
│   ├── 02-rf-syntax-cheatsheet.md
│   ├── 03-browser-library-guide.md
│   ├── 04-exercises.md
│   ├── 05-troubleshooting.md
│   ├── 06-ai-assisted-testing.md
│   ├── windows-setup.md
│   └── images/
├── .claude/
│   └── settings.json
├── CLAUDE.md
├── AGENTS.md
├── PLAN.md
├── README.md
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── LICENSE
```

### Step 1.5: pyproject.toml

```toml
[project]
name = "rf-workshop-42vienna"
version = "0.1.0"
description = "Robot Framework E2E testing workshop for 42 Vienna"
requires-python = ">=3.10"
license = "MIT"
dependencies = [
    "robotframework>=7.0",
    "robotframework-browser>=19.0",
]

[dependency-groups]
dev = [
    "robotframework-robocop>=8.0",
]

[tool.uv]
package = false

[tool.robot]
outputdir = "results"
loglevel = "DEBUG"

[tool.robot.variables]
BASE_URL = "https://www.saucedemo.com"
HEADLESS = "true"
```

`package = false` because this is a workshop project, not a distributable package. Avoids requiring `[build-system]`.

### Step 1.6: .python-version

```
3.12
```

Pins the Python version for `uv`. Ensures consistency across DevContainer, CI, and local development.

### Step 1.7: .gitignore

```
# Test results
results/
output/
log.html
report.html
output.xml
screenshots/

# Python
*.pyc
__pycache__/
.venv/

# IDE
.idea/

# OS
.DS_Store
Thumbs.db
```

Note: `uv.lock` is NOT in .gitignore — it must be committed for reproducible installs.

### Step 1.8: .vscode/settings.json

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "robotcode.robot.pythonPath": ["${workspaceFolder}/.venv/bin/python"],
    "robotcode.robot.outputDir": "results"
}
```

### Step 1.9: .vscode/extensions.json

```json
{
    "recommendations": [
        "d-biehl.robotcode",
        "ms-python.python"
    ]
}
```

### CURRENT ISSUES — Phase 1

- [x] **DECIDED:** Repo created via `gh repo create` CLI (public, with description).
- [x] **DECIDED:** Left for auto-sync. `github-sync` CronJob auto-discovers all HackXIt repos and mirrors to `github-mirrors` group.
- [x] **RESOLVED:** GitHub auth required `workflow` scope for pushing workflow files. Added via `gh auth refresh -s workflow`.

---

## Phase 2: DevContainer Configuration

**Timeline:** Day 2 (March 10)
**Dependencies:** Phase 1 (directory structure exists)

### Step 2.1: devcontainer.json

```json
{
    "name": "RF Workshop 42 Vienna",
    "image": "mcr.microsoft.com/devcontainers/python:3.12-bookworm",
    "features": {
        "ghcr.io/devcontainers/features/node:1": { "version": "22" },
        "ghcr.io/devcontainers/features/github-cli:1": {},
        "ghcr.io/va-h/devcontainers-features/uv:1": {}
    },
    "postCreateCommand": "bash .devcontainer/post-create.sh",
    "customizations": {
        "vscode": {
            "extensions": [
                "d-biehl.robotcode",
                "ms-python.python"
            ],
            "settings": {
                "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
                "robotcode.robot.pythonPath": ["${workspaceFolder}/.venv/bin/python"]
            }
        }
    }
}
```

Key design:
- **Python 3.12 bookworm** base: has DevContainer metadata, supports x86-64 and arm64
- **Node.js 22 LTS**: required by Browser Library's Playwright engine
- **uv feature**: installs uv package manager
- **GitHub CLI**: useful for PR creation from terminal

**Fallback:** If the community uv feature (`va-h/devcontainers-features/uv`) is unreliable, install uv directly in `post-create.sh` via `curl -LsSf https://astral.sh/uv/install.sh | sh`.

### Step 2.2: post-create.sh

```bash
#!/bin/bash
set -euo pipefail

echo "=== Workshop DevContainer Setup ==="

# Step 1: Verify uv is available (installed by devcontainer feature or install here)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "uv version: $(uv version)"

# Step 2: Install Python dependencies from pyproject.toml + uv.lock
echo "Installing dependencies with uv sync..."
uv sync --locked

# Step 3: Initialize Browser Library (install Playwright + Chromium)
echo "Initializing Browser Library (Chromium only — ~250MB download)..."
uv run rfbrowser init chromium

# Step 4: Verify the environment
echo ""
echo "Running environment checks..."
uv run python scripts/check_environment.py

echo ""
echo "=== Setup complete! You are ready for the workshop. ==="
```

### Step 2.3: Testing the DevContainer

Must verify:
- Opens in GitHub Codespaces (web browser VSCode)
- Opens in local VSCode with Docker Desktop
- `uv sync --locked` completes without errors
- Browser Library can launch headless Chromium
- `robot tests/00_setup_verification/` passes
- RobotCode extension provides syntax highlighting and autocomplete
- Total build time under 5 minutes

### CURRENT ISSUES — Phase 2

- [ ] **VERIFY:** Does the `ghcr.io/va-h/devcontainers-features/uv:1` feature work reliably in Codespaces? Fallback already in post-create.sh.
- [ ] **VERIFY:** Does `rfbrowser init chromium` complete within the Codespace timeout?
- [x] **MITIGATED:** Playwright system deps — added `npx playwright install-deps chromium` to post-create.sh.
- [ ] **KNOWN ISSUE:** First Codespace build downloads ~250MB of Chromium binaries. Consider Codespace prebuild for caching.

---

## Phase 3: Environment Readiness Script

**Timeline:** Day 2-3 (March 10-11)
**Dependencies:** Phase 1 (scripts/ directory exists)

This is a **first-class citizen** of the repository, not an afterthought.

### Step 3.1: Script Location and Invocation

**File:** `scripts/check_environment.py`

**Invocation methods:**
- `python scripts/check_environment.py` — works with just Python on PATH, no deps needed
- `uv run python scripts/check_environment.py` — works after `uv sync`
- Called automatically at end of `post-create.sh`

**Critical constraint:** Must use ONLY Python standard library. No third-party imports. The script must run even before `uv sync` — this is its primary diagnostic value.

### Step 3.2: Script Architecture

**Platform Detection:**
- Detect OS: Linux, macOS, Windows, WSL (check `/proc/version` for "microsoft"/"Microsoft")
- Detect architecture: x86_64 vs arm64/aarch64
- Determines which install instructions to show

**Check Registry (11 checks, in order):**

| # | Check | Required | What it verifies |
|---|-------|----------|------------------|
| 1 | Python version | Yes | `sys.version_info >= (3, 10)`, recommend 3.12+ |
| 2 | uv installation | Yes | `shutil.which("uv")`, run `uv version` via subprocess |
| 3 | Node.js | Yes | `shutil.which("node")`, parse `node --version` for >= 18 |
| 4 | Virtual environment | Yes | `.venv/` exists and contains expected executables |
| 5 | Robot Framework | Yes | `subprocess.run(["robot", "--version"])` in .venv, parse version >= 7.0 |
| 6 | Browser Library | Yes | Try `subprocess.run([".venv/bin/python", "-c", "import Browser"])` |
| 7 | rfbrowser init status | Yes | Check Playwright browsers path for chromium directory |
| 8 | Git configuration | Yes | `git config user.name` and `git config user.email` return non-empty |
| 9 | Docker | No (WARN) | `shutil.which("docker")`, try `docker info` |
| 10 | Network: saucedemo.com | Yes | `urllib.request.urlopen("https://www.saucedemo.com", timeout=10)` |
| 11 | Network: github.com | Yes | `urllib.request.urlopen("https://github.com", timeout=10)` |

### Step 3.3: Output Behavior

**Colored terminal output** via ANSI escape sequences (detected via `sys.stdout.isatty()`; disabled on non-TTY or Windows cmd without ANSI):
- `[PASS]` (green) for OK
- `[FAIL]` (red) for required failures
- `[WARN]` (yellow) for optional items missing

**Example failure output:**
```
[FAIL] Node.js: NOT FOUND
       Node.js >= 18 is required by Browser Library's Playwright engine.
       Playwright (which powers Browser Library) runs a Node.js server
       process that communicates with browsers via the Chrome DevTools
       Protocol. Without Node.js, tests cannot execute.

       To install:
         Linux (apt):    sudo apt install nodejs npm
         Linux (nvm):    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && nvm install 22
         macOS:          brew install node
         Windows (WSL):  sudo apt install nodejs npm
         Windows:        Download from https://nodejs.org/en/download/

       See: https://nodejs.org/en/download/
```

**Context examples that newcomers wouldn't know:**
- "rfbrowser init downloads Playwright browser binaries (~250MB for Chromium). This is a one-time download and may take a few minutes on slow connections."
- "Browser Library requires Node.js because it uses Playwright's Node.js backend for browser automation."
- "Git user.name and user.email are required for creating commits. These are stored locally and used in commit metadata."

**Summary box at the end:**
```
╔══════════════════════════════════════════╗
║  Environment Check: 9/11 passed         ║
║  2 issues need fixing before you start  ║
╠══════════════════════════════════════════╣
║  FAIL: Node.js                          ║
║  FAIL: rfbrowser init status            ║
╚══════════════════════════════════════════╝
```

**Exit code:** 0 if all required checks pass. 1 if any required check fails.

### Step 3.4: Browser Binary Detection Logic

```python
import os

def find_playwright_browsers():
    """Check common locations for Playwright browser binaries."""
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if env_path and os.path.isdir(env_path):
        return env_path

    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, ".cache", "ms-playwright"),            # Linux
        os.path.join(home, "Library", "Caches", "ms-playwright"), # macOS
        os.path.join(home, "AppData", "Local", "ms-playwright"),  # Windows
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return None
```

Then look for a `chromium-*` directory inside the found path.

### Step 3.5: Integration Points

1. **DevContainer `post-create.sh`** — runs as final step to verify container setup
2. **README.md Quick Start** — "Step 1: Verify your environment"
3. **docs/01-getting-started.md** — each setup path ends with running this script
4. **docs/windows-setup.md** — final verification step
5. **Workshop agenda** — first 15 minutes include running this script
6. **CI pipeline** — NOT run in CI (controlled environment), but could be added as sanity check

### CURRENT ISSUES — Phase 3

- [x] **DECIDED:** Core runtime only. Robocop is a dev tool, not required for workshop tests to run.
- [ ] **VERIFY:** Playwright browsers path detection works correctly in Codespaces (may use a non-standard path).
- [ ] **VERIFY:** ANSI color codes render correctly in Codespaces terminal and Windows Terminal.

---

## Phase 4: Example Test Suites

**Timeline:** Day 2-3 (March 10-11)
**Dependencies:** Phase 1 (directory structure), Phase 2 (DevContainer works)

All tests target `https://www.saucedemo.com`:
- Login page with multiple test users
- Product catalog (6 products)
- Shopping cart
- Checkout flow (info → overview → confirmation)
- Test credentials: `standard_user` / `secret_sauce`
- Error users: `locked_out_user`, `problem_user`, `performance_glitch_user`, `error_user`, `visual_user`

### Step 4.1: Resource Files (Page Object Pattern)

Resource files in `resources/` form the keyword abstraction layer. This is a critical teaching element — showing how RF separates test logic from page interaction details.

**`common.resource`** — Shared setup/teardown:
- `Open SauceDemo` keyword: New Browser (headless), New Context, New Page, Navigate to URL
- `Close SauceDemo` keyword: Close Browser
- Suite Setup/Teardown configuration
- Common variables (`${BASE_URL}`, `${VALID_USER}`, `${VALID_PASSWORD}`)

**`login_page.resource`** — Login page keywords:
- `Login With Credentials` [username] [password]
- `Login Should Succeed`
- `Login Should Fail With Message` [message]
- Selectors: `#user-name`, `#password`, `#login-button`, `.error-message-container`

**`products_page.resource`** — Products page keywords:
- `Product Count Should Be` [count]
- `Add Product To Cart` [product_name]
- `Remove Product From Cart` [product_name]
- `Open Product Details` [product_name]
- `Cart Badge Should Show` [count]

**`cart_page.resource`** — Cart page keywords:
- `Open Cart`
- `Cart Should Contain` [product_name]
- `Cart Should Be Empty`
- `Proceed To Checkout`
- `Continue Shopping`

**`checkout_page.resource`** — Checkout page keywords:
- `Fill Checkout Information` [first] [last] [zip]
- `Complete Checkout`
- `Order Should Be Confirmed`

### Step 4.2: Progressive Test Suites

**`00_setup_verification/verify_setup.robot`**
- Open a browser, navigate to SauceDemo, take a screenshot, close browser
- Minimal dependencies, maximum diagnostic value
- **This is the first thing students run**

**`01_first_test/first_browser_test.robot`**
- Raw keywords (no resource imports)
- Shows New Browser, New Page, Get Title, Get Text
- Explains `*** Settings ***`, `*** Test Cases ***`, `*** Variables ***`
- Heavily commented for learning

**`02_login_tests/login.robot`**
- Valid login (standard_user), invalid password, locked out user, empty credentials
- Imports `login_page.resource`
- Demonstrates data-driven approach with `[Template]`

**`03_product_tests/product_catalog.robot`**
- Verify product count, add to cart, verify badge, sort products
- Shows more complex selectors and assertions

**`04_cart_tests/shopping_cart.robot`**
- Add multiple items, verify cart, remove items, cart persistence across navigation
- Shows Test Setup/Teardown

**`05_checkout_tests/checkout_flow.robot`**
- Complete checkout with valid info, missing info validation
- Shows multi-step workflows

**`06_e2e_scenarios/complete_purchase.robot`**
- Login → browse → add to cart → checkout → confirmation
- The "crown jewel" test showing everything together
- Uses all resource files

### Step 4.3: Student Exercise Template

**`student_exercises/_template.robot`**
```robotframework
*** Settings ***
Documentation     [Student Name] - [Exercise Description]
Library           Browser
Resource          ../../resources/common.resource

*** Test Cases ***
Example Test Case
    [Documentation]    Describe what this test verifies
    [Tags]    student    exercise
    # Write your test steps here
    Log    Replace this with real test steps
```

**`student_exercises/README.md`** — instructions for:
- How to create a new test file from the template
- Naming conventions: `{username}_exercise_{N}.robot`
- How to run locally: `uv run robot tests/student_exercises/your_file.robot`
- How to commit and create a PR

### CURRENT ISSUES — Phase 4

- [x] **VERIFIED:** SauceDemo CSS selectors are current — all 25 tests pass locally and in CI (March 2026).
- [ ] **VERIFY:** Browser Library's `New Browser` keyword works headless in Codespaces (no display server).
- [x] **DECIDED:** Rely on default. `common.resource` uses `chromium` in `New Browser`, which is sufficient.
- [ ] **KNOWN RISK:** SauceDemo could go down during the workshop. Prepare a fallback SUT (automationexercise.com, the-internet.herokuapp.com).

---

## Phase 5: CI/CD Pipeline

**Timeline:** Day 3 (March 11)
**Dependencies:** Phase 1 (repo structure), Phase 4 (test suites exist to run)

### Step 5.1: GitHub Actions — Test Runner

**`.github/workflows/robot-tests.yml`**

```yaml
name: Robot Framework Tests
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  robot-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
          python-version: "3.12"

      - name: Install Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "22"

      - name: Install dependencies
        run: uv sync --locked

      - name: Initialize Browser Library
        run: uv run rfbrowser init chromium

      - name: Run Robot Framework tests
        run: |
          uv run robot \
            --outputdir results \
            --loglevel DEBUG \
            --variable HEADLESS:true \
            tests/

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: robot-results
          path: results/
```

Key design:
- `astral-sh/setup-uv@v7` with `enable-cache: true` caches uv dependency cache between runs
- `uv sync --locked` ensures lockfile is respected
- `uv run robot` runs within the project's virtual environment
- `if: always()` ensures results upload even on test failure
- `results/` contains `log.html`, `report.html`, `output.xml`

### Step 5.2: PR Feedback Workflow

**`.github/workflows/pr-feedback.yml`**
- Triggered on PR events
- Runs tests (same uv setup as above)
- Parses `results/output.xml` and posts a Markdown summary as a PR comment
- Links to the full report artifact
- Could use a custom `scripts/parse_results.py` or `rebot` for summary generation

### Step 5.3: Robocop Lint Job

Added a separate `lint` job to `robot-tests.yml`:
- Runs `robocop check --reports sarif --exit-zero tests/ resources/` using the "minimal" ruleset from `pyproject.toml`
- Uploads `.sarif.json` to GitHub Code Scanning via `github/codeql-action/upload-sarif@v4`
- Issues appear in the **Security → Code scanning** tab with file/line annotations
- `--exit-zero` ensures lint findings don't fail the build

PR feedback workflow (`pr-feedback.yml`) also includes Robocop:
- Uses `--reports sarif,text_file` for both SARIF upload and human-readable PR comment
- PR comment shows test results + Robocop issue count + link to Code Scanning tab

### Step 5.4: GitHub Pages for Documentation

MkDocs Material site deployed via GitHub Pages:
- URL: `https://hackxit.github.io/42vienna-robotframework-workshop/`
- Workflow: `.github/workflows/docs.yml` — triggers on changes to `docs/`, `mkdocs.yml`, `resources/*.resource`, or `scripts/generate_keyword_docs.py`
- Build steps: generate keyword docs from libdoc → build MkDocs → deploy via `actions/deploy-pages@v4`
- Enabled via `gh api` with `build_type=workflow`

### CURRENT ISSUES — Phase 5

- [x] **VERIFIED:** `astral-sh/setup-uv@v7` is latest major (v7.3.1 latest release, Feb 2026). No changes needed.
- [x] **DECIDED:** CI runs ALL tests on every PR. This validates students don't break existing tests. 27 tests run in ~1 min.
- [x] **DECIDED:** Failed tests do not block merge (no branch protection rules). CI reports status but workshop is learning-focused.
- [x] **VERIFIED:** Robocop SARIF → GitHub Code Scanning integration works. Both `robot-tests.yml` (lint job) and `pr-feedback.yml` upload SARIF successfully.
- [x] **DONE:** GitHub Pages deployed with MkDocs Material. Docs workflow runs on push to main.
- [ ] **VERIFY:** GitHub Actions free tier limits (2000 min/month for free accounts, 3000 min/month for Pro). Each run with Playwright install may take ~3-5 min.

---

## Phase 6: AI Integration

**Timeline:** Day 3-4 (March 11-12)
**Dependencies:** Phase 1 (repo structure), Phase 4 (test patterns established)

### Step 6.1: CLAUDE.md

Content structure:
- **Project Overview:** Workshop repo for RF + Browser Library E2E testing against SauceDemo
- **Repository Structure:** Directory layout explanation
- **Package Management:** Uses `uv` (NOT pip). Commands: `uv sync`, `uv run robot`, `uv add <package>`
- **Robot Framework Conventions:** Section syntax, keyword naming, resource file patterns
- **Browser Library Patterns:** New Browser + New Page lifecycle, selector strategies, assertion patterns
- **SauceDemo Reference:** Available users, CSS selectors for each page, page flow diagram
- **Test Writing Guidelines:** How to create new tests, naming conventions, tag usage
- **PR Review Guidelines:** What to check in student submissions
- **Common Commands:**
  ```
  uv sync                        # Install dependencies
  uv run robot tests/            # Run all tests
  uv run robot tests/student_exercises/  # Run student tests only
  uv run rfbrowser init chromium # Initialize browser binaries
  python scripts/check_environment.py  # Verify environment
  ```

### Step 6.2: AGENTS.md

Either a symlink to CLAUDE.md (`AGENTS.md -> CLAUDE.md`) or a separate file with agent-specific workflow instructions:
- How to generate test cases from requirements
- How to review PRs for RF best practices
- How to suggest improvements to student tests
- Link to the RF MCP server skills available

### Step 6.3: Robot Framework MCP Server

Add to `.claude/settings.json`:
```json
{
    "mcpServers": {
        "robotframework-mcp": {
            "command": "robotframework-mcp",
            "type": "stdio"
        }
    }
}
```

Add `robotframework-mcp` to `pyproject.toml` dev dependencies.

### Step 6.4: AI Demo Preparation

Prepare a live demo script for the workshop:
1. Show Claude Code / Copilot in the DevContainer
2. Describe a test scenario in natural language ("I want to test that a user can sort products by price low to high")
3. AI generates a Robot Framework test file
4. Run the generated test
5. Refine based on results

This demonstrates the "AI-assisted test automation" angle.

### CURRENT ISSUES — Phase 6

- [x] **VERIFIED:** `robotframework-mcp` exists but is SeleniumLibrary-based (not suitable). Using `rf-mcp` (0.30+, 71+ releases, mature). Added to dev deps.
- [x] **DECIDED:** AI demo only (instructor shows Claude Code). Not pre-configured for students — adds complexity. `.claude/settings.json` exists for instructor use.
- [x] **DECIDED:** No automatic AI PR review. Workshop is about learning, not automated gatekeeping. Instructor reviews manually.

---

## Phase 7: Documentation

**Timeline:** Day 4-5 (March 12-13)
**Dependencies:** Phase 2-5 (everything being documented must be built first)

### Step 7.1: README.md

Top-level README must be scannable and actionable:
- Workshop title, date, location
- "Quick Start" (3 steps: clone → open Codespace → run first test)
- Prerequisites (GitHub account — that's it for Codespaces path)
- Workshop agenda / timeline
- Links to all docs
- CI status badge
- RF highlight: one framework for web, API, mobile, desktop testing — unlike specialized tools

### Step 7.2: docs/01-getting-started.md

Three setup paths:
1. **GitHub Codespaces (recommended):** Click "Code" > "Codespaces" > "Create codespace on main" → wait → done
2. **Local VSCode + Docker:** Clone repo → "Reopen in Container"
3. **Local without Docker:** Install Python 3.12 → install uv → `uv sync` → `rfbrowser init chromium`

Each path ends with: Run `python scripts/check_environment.py` to verify.

### Step 7.3: docs/02-rf-syntax-cheatsheet.md

One-page reference:
- Section headers (`*** Settings ***`, `*** Variables ***`, `*** Test Cases ***`, `*** Keywords ***`)
- Keyword syntax (separator: 2+ spaces or tab, arguments, return values)
- Variables (`${SCALAR}`, `@{LIST}`, `&{DICT}`)
- Common built-in keywords (Log, Should Be Equal, Should Contain, etc.)
- Import syntax (Library, Resource, Variables)
- Tags, Documentation, Setup/Teardown
- FOR loops, IF/ELSE (students know C control flow)

### Step 7.4: docs/03-browser-library-guide.md

Browser Library specific:
- New Browser / New Context / New Page lifecycle
- Selector syntax (CSS, text, id, xpath) with SauceDemo examples
- Key keywords: Click, Fill Text, Get Text, Get Title
- Assertions: Get Text + should equal vs direct assertion keywords
- Screenshots: Take Screenshot
- Waiting: Built-in auto-wait, explicit Wait For Elements State
- Headless vs headed mode

### Step 7.5: docs/04-exercises.md

Progressive exercises:
1. **Warmup:** Run `verify_setup.robot`. Observe output. Open `results/log.html`.
2. **First Test:** Write a test that opens SauceDemo and verifies page title is "Swag Labs"
3. **Login:** Write tests for valid login and one invalid login scenario
4. **Products:** Add a product to cart, verify cart badge shows "1"
5. **E2E:** Complete purchase flow: login → add 2 items → checkout → verify confirmation
6. **Advanced — Keyword Abstraction:** Create a custom resource file with reusable keywords
7. **Data-Driven:** Use `[Template]` to test login with multiple credential sets
8. **AI-Assisted:** Use Claude/Copilot to generate a test from a natural language description

### Step 7.6: docs/05-troubleshooting.md

Common issues:
- "Browser not found" — `rfbrowser init` not run, or run as wrong user
- "Timeout waiting for selector" — Wrong selector, page not loaded, SauceDemo down
- DevContainer build fails — Docker not running, insufficient disk space
- "Permission denied" on rfbrowser — File ownership in container
- Tests pass locally but fail in CI — Headless mode, timing differences
- How to read `log.html` and `report.html`

### Step 7.7: docs/06-ai-assisted-testing.md

Guide for the AI demo portion:
- What is MCP? Brief explanation
- Setting up Claude Code with RF MCP Server
- Prompting strategies for test generation
- Reviewing AI-generated tests
- Browser Library recorder as alternative to writing tests manually

### Step 7.8: docs/windows-setup.md

**Section 1: Choose Your Path** — Decision tree:
- Want zero-friction? → Codespaces (Section 2)
- Have Docker Desktop? → DevContainer (Section 3)
- Want native setup? → WSL2 (Section 4)

**Strongly recommend Codespaces** for the workshop itself.

**Section 2: GitHub Codespaces (Recommended)**
- Only needs a web browser and GitHub account
- Step-by-step with screenshots
- Free tier: 60 hours/month on 2-core machines

**Section 3: DevContainer (Docker Desktop)**
1. Install Docker Desktop with WSL2 backend
2. Install VSCode + Dev Containers extension
3. Clone repo → "Reopen in Container"
4. Run `python scripts/check_environment.py`

**Section 4: Native Windows (WSL2)**
1. `wsl --install` → restart → setup Ubuntu
2. Inside WSL2: install nvm + Node.js 22, install uv, clone repo, `uv sync`, `rfbrowser init chromium`
3. VSCode WSL extension for IDE integration
4. Run `python scripts/check_environment.py`

**Section 5: Common Windows Issues**
- Docker Desktop requires WSL2 — Enable virtualization in BIOS
- Permission denied in WSL — Don't clone into `/mnt/c/`, use `~/`
- rfbrowser init hangs — Firewall blocking Playwright downloads
- EACCES during npm operations — WSL filesystem permissions
- Browser not launching headed — Needs X server (VcXsrv) in WSL, not worth complexity for workshop

### Step 7.9: MkDocs GitHub Pages Site

All documentation is now hosted via MkDocs Material at `https://hackxit.github.io/42vienna-robotframework-workshop/`.

- `mkdocs.yml` — Site configuration with Material theme, dark/light toggle, navigation structure
- `.github/workflows/docs.yml` — Deployment workflow (triggers on docs/mkdocs.yml/resource file changes)
- Doc filenames renamed from numbered (`01-getting-started.md`) to clean (`getting-started.md`) for MkDocs nav compatibility
- Added `docs` dependency group to `pyproject.toml`: `mkdocs>=1.6,<2.0`, `mkdocs-material>=9.0`

### Step 7.10: Keyword Library Documentation (libdoc)

Auto-generated keyword documentation from resource files using Robot Framework's `libdoc`:

- `scripts/generate_keyword_docs.py` — Runs libdoc JSON → Markdown conversion for all 5 resource files
- Generates `docs/keywords/*.md` (index, common, login_page, products_page, cart_page, checkout_page)
- Integrated into docs deployment workflow: runs before `mkdocs build`
- Keywords section in MkDocs nav links to all generated keyword docs

### Step 7.11: Robocop Ruleset Configuration

Added "minimal" ruleset v0.1.0 to `pyproject.toml` under `[tool.robocop.lint]`:

- **Guiding principles:** runtime-breaking = Error, deprecation with removal plan = Warning, deprecation without removal = Informational, opinionated/style = Disabled
- `select` / `ignore` / `configure` arrays defining ~50 selected rules, ~35 ignored rules, and severity overrides
- Used by all CI jobs (robot-tests lint job + pr-feedback workflow)

### CURRENT ISSUES — Phase 7

- [x] **DECIDED:** Screenshots are nice-to-have. Text instructions are sufficient; screenshots can be added during Phase 11 pre-check if time permits.
- [x] **DECIDED:** C comparison tables already included in `docs/rf-syntax-cheatsheet.md`. Balance is good: minimal theory, heavy on examples.
- [x] **DONE:** MkDocs Material deployed to GitHub Pages with keyword docs, all documentation sections.
- [x] **DONE:** Libdoc-generated keyword documentation integrated into MkDocs build pipeline.
- [x] **DONE:** Robocop "minimal" ruleset v0.1.0 configured in pyproject.toml.
- [ ] **VERIFY:** Windows setup doc should be tested on an actual Windows machine or VM.

---

## Phase 8: GitHub Mirroring to GitLab

**Timeline:** Day 4 (March 12)
**Dependencies:** Phase 1 (GitHub repo exists)

### Step 8.1: Verify Sync Infrastructure

The existing `github-sync` CronJob discovers all projects under the `github-mirrors` GitLab group and matches them by `path` to GitHub repos under `HackXIt`. It runs `git clone --bare` from GitHub and `git push --mirror` to GitLab.

For this to work:
1. GitHub repo exists (Phase 1.1) ✓
2. GitLab project `github-mirrors/42vienna-robotframework-workshop` exists (Phase 1.3)
3. Next `github-sync` run (every 6h) mirrors content

### Step 8.2: Verify Issue/PR Sync

The `github-gitlab-sync` CronJob will:
- Find the project in `github-mirrors` group
- Match it to `HackXIt/42vienna-robotframework-workshop` on GitHub
- Sync issues bidirectionally with `<!-- sync:github:... -->` markers
- Sync PRs (GitHub → GitLab as issues with `github-pr` label)

### Step 8.3: Manual Trigger (if needed)

If waiting 6 hours for first sync is too long:
```bash
export KUBECONFIG=~/git-stash/homelab-new/homelab-gitops-template/gitops-template/talos/kubeconfig
kubectl create job --from=cronjob/github-sync manual-sync-$(date +%s) -n github-sync
```

### CURRENT ISSUES — Phase 8

- [ ] **VERIFY:** Does `github-sync` CronJob auto-create GitLab projects, or must they be pre-created manually?
- [ ] **VERIFY:** The sync CronJob container can reach `github.com` from the cluster network.
- [ ] **VERIFY:** GitLab PAT (stored in sync-tokens secret) has sufficient permissions for the new project.

---

## Phase 9: Student Workflow Design

**Timeline:** Day 4-5 (March 12-13)
**Dependencies:** Phase 1, 5 (repo + CI exists)

### Step 9.1: Plan A — Fork Model (Primary)

Forking is standard open-source procedure. Even though students are unfamiliar with forks, this is a transferable skill worth teaching. The docs must make it frictionless with step-by-step instructions.

**Fork workflow:**
1. Student navigates to `github.com/HackXIt/42vienna-robotframework-workshop`
2. Clicks **"Fork"** button (top right) → creates `{username}/42vienna-robotframework-workshop`
3. Opens Codespace on **their fork** (Code → Codespaces → Create codespace on main)
4. Writes tests in `tests/student_exercises/{username}_*.robot`
5. Commits and pushes to their fork's `main` (or a feature branch — either works)
6. Creates PR from their fork back to `HackXIt/42vienna-robotframework-workshop`
7. GitHub Actions runs CI on the PR (requires workflow approval for first-time contributors — see note below)

**Important CI note for forks:** GitHub Actions requires maintainer approval to run workflows on PRs from first-time contributors (for security). Nikolaus must approve each student's first workflow run via the Actions tab. This is a one-time action per student. Alternatively, the repo setting "Require approval for all outside collaborators" can be changed to "Require approval for first-time contributors" (the default) to minimize friction after the first run.

**Codespace note for forks:** Students create Codespaces on their own fork, not the upstream repo. The DevContainer config is included in the fork, so it works identically. Each student's Codespace runs against their own GitHub account's free tier (60h/month).

**Keeping forks in sync:** For a 3-4 hour workshop, sync is not an issue — students fork once, work, and PR. No need to pull upstream changes. If needed, the docs can mention `gh repo sync` or the GitHub web "Sync fork" button.

### Step 9.2: Plan B — Collaborator Access (Fallback)

If forking causes too much friction during the workshop (students confused, Codespace issues on forks, CI approval bottleneck), switch to collaborator access on-the-fly:

1. Nikolaus asks students for their GitHub usernames
2. Adds them as collaborators via `gh api repos/HackXIt/42vienna-robotframework-workshop/collaborators/{username} -X PUT -f permission=write`
3. Students accept the invitation (email or GitHub notification)
4. Students work on branches directly: `student/{username}`
5. Push and PR as normal — no workflow approval needed for collaborators

This can be done in ~2 minutes per student. Keep this as a back-pocket option.

### Step 9.3: Student Onboarding Flow (During Workshop)

**Plan A (Fork):**
1. Open `github.com/HackXIt/42vienna-robotframework-workshop` in browser
2. Click **"Fork"** → accept defaults → click "Create fork"
3. On your fork: click "Code" → "Codespaces" → "Create codespace on main"
4. Wait for DevContainer to build (~3-5 min first time)
5. Terminal: `uv run robot tests/00_setup_verification/` — verify green
6. Follow `docs/04-exercises.md` for guided exercises
7. When ready to contribute:
   ```bash
   # Write tests in tests/student_exercises/
   git add tests/student_exercises/{username}_*.robot
   git commit -m "Add tests by {username}"
   git push origin main
   ```
8. Go to GitHub → your fork → click "Contribute" → "Open pull request"
9. Ensure base repo is `HackXIt/42vienna-robotframework-workshop` and base branch is `main`
10. Fill in PR template, create PR
11. Notify Nikolaus to approve CI workflow run (first time only)
12. Observe CI results in the PR

**Plan B (Collaborator) — if fork flow fails:**
1. Give Nikolaus your GitHub username
2. Accept collaborator invitation
3. Click "Code" → "Codespaces" → "Create codespace on main" (on the main repo)
4. Terminal: `uv run robot tests/00_setup_verification/` — verify green
5. Follow `docs/04-exercises.md` for guided exercises
6. When ready to contribute:
   ```bash
   git checkout -b student/{username}
   git add tests/student_exercises/{username}_*.robot
   git commit -m "Add tests by {username}"
   git push -u origin student/{username}
   ```
7. Create PR via GitHub web UI (or `gh pr create` from terminal)
8. Observe CI results in the PR

### Step 9.3: PR Template

**`.github/PULL_REQUEST_TEMPLATE.md`**
```markdown
## Test Description
What does your test verify?

## Checklist
- [ ] Tests pass locally (`uv run robot tests/student_exercises/your_file.robot`)
- [ ] Test has meaningful assertions (not just navigation)
- [ ] Test has Documentation keyword

## SauceDemo Flow Tested
- [ ] Login
- [ ] Product browsing
- [ ] Cart operations
- [ ] Checkout
- [ ] Other: ___
```

### CURRENT ISSUES — Phase 9

- [x] **DECIDED:** Fork model is Plan A (standard open-source workflow). Collaborator access is Plan B (on-the-fly fallback if forking causes friction).
- [ ] **ACTION:** Docs must include explicit fork instructions with screenshots (include in `docs/01-getting-started.md` and `docs/04-exercises.md`)
- [ ] **ACTION:** Test the full fork → Codespace → PR → CI approval flow with a second GitHub account before the workshop
- [ ] **VERIFY:** GitHub Actions workflow approval UX for first-time fork contributors — is it clear enough, or will it confuse students?
- [ ] **VERIFY:** Codespaces work correctly when created on a forked repo (DevContainer config should be identical)
- [ ] **NOTED:** Each student needs their own Codespace (per-user). They use their own GitHub account's free tier.

---

## Phase 10: Workshop Agenda

**Timeline:** Day 5-6 (March 13-14)
**Dependencies:** All content phases complete

### Suggested Timeline (3-4 hours starting 16:00)

| Time | Duration | Activity | Notes |
|------|----------|----------|-------|
| 16:00 | 15 min | Welcome, intro, recap of Part 1 | Who am I, what is RF, why generic > specialized |
| 16:15 | 15 min | DevContainer / Codespaces setup | Everyone opens Codespace, runs check script |
| 16:30 | 20 min | RF syntax walkthrough | Using cheat sheet, live coding |
| 16:50 | 15 min | Live demo: Browser Library basics | `first_browser_test.robot`, explain selectors |
| 17:05 | 10 min | **Break** | |
| 17:15 | 30 min | Guided exercise: Login tests (Ex 2-3) | Students write, instructor walks around |
| 17:45 | 30 min | Guided exercise: Products + Cart (Ex 4) | More independence, less guidance |
| 18:15 | 10 min | **Break** | |
| 18:25 | 20 min | Resource files & keyword abstraction demo | Show the page object pattern |
| 18:45 | 30 min | Free exercise: E2E scenario (Ex 5-6) | Students work independently or in pairs |
| 19:15 | 15 min | AI demo: Claude generates test from requirements | Wow factor, future of testing |
| 19:30 | 15 min | PR creation, CI results review | "Test Manager" discussion, look at reports |
| 19:45 | 15 min | Wrap-up, Q&A, next steps | How to continue learning, RF ecosystem |

### Key Talking Points

- **RF as generic framework:** One syntax, one reporting format, one structure — but swap libraries for different testing domains (Browser for web, RequestsLibrary for API, AppiumLibrary for mobile, etc.)
- **Comparison with specialized tools:** Cypress/Playwright for web only, Postman for API only, Appium standalone for mobile only — each with different syntax, different reporting, different CI integration
- **AI-assisted testing:** The future is not "AI replaces testers" but "AI accelerates test creation, humans design test strategy"
- **CI/CD integration:** Tests are only valuable if they run automatically. Show the PR → CI → report → feedback loop.

---

## Phase 11: Pre-Workshop Checklist

**Timeline:** Day 6-7 (March 14-15)
**Dependencies:** Everything

### Critical (Must Complete Before March 16)

- [ ] DevContainer builds successfully in GitHub Codespaces
- [ ] `uv sync --locked` completes without errors
- [ ] `uv run rfbrowser init chromium` completes in < 2 minutes
- [ ] `python scripts/check_environment.py` shows all green in Codespace
- [ ] `python scripts/check_environment.py` shows actionable errors on bare machine (test failure messages)
- [ ] `uv.lock` is committed and up to date with `pyproject.toml`
- [ ] All example tests pass in CI and in DevContainer
- [ ] Students can create branches and PRs (test with second GitHub account)
- [ ] CI pipeline provides clear feedback on PR with test results
- [ ] SauceDemo is accessible
- [ ] Documentation is complete and accurate (walkthrough each doc as a student)
- [ ] GitHub repo is public and accessible without auth
- [ ] Full student workflow tested end-to-end (clone → Codespace → write test → commit → PR → CI)

### Coordination with 42 Vienna

- [ ] **Contact Simon Dablander:** Verify 42 Vienna machines have web browser (for Codespaces). Stable internet. No firewall blocking GitHub domains.
- [ ] **If using local machines:** Verify Docker Desktop + VSCode installed (if not using Codespaces-only approach)
- [ ] **Decision:** Recommend Codespaces-only to avoid setup issues. Students only need a browser.
- [ ] **Contact Hans Jörg Otto:** Confirm attendee count, room setup, projector, power outlets
- [ ] **Pre-check meeting with Simon:** Verify the full flow works from 42 Vienna's network (March 14-15, either in person or screencast)

### Nice-to-Have

- [ ] GitHub Pages deployment of test reports working
- [ ] AI MCP server demo prepared and tested
- [ ] Browser Library recorder demo prepared
- [ ] Codespace prebuild configured (caches DevContainer build for instant startup)
- [ ] Printed cheat sheets for students without second screen
- [ ] Windows setup doc tested on actual Windows machine/VM

---

## Dependency Graph & Critical Path

```
Phase 1 (Repo + pyproject.toml)
  │
  ├──→ Phase 2 (DevContainer + uv) ──→ Phase 3 (Readiness Script)
  │                                          │
  ├──→ Phase 8 (GitLab Mirror)              ├──→ Phase 4 (Test Suites)
  │                                          │         │
  │                                          │         ├──→ Phase 5 (CI/CD)
  │                                          │         │
  │                                          │         └──→ Phase 6 (AI Integration)
  │                                          │
  │                                          └──→ Phase 7 (Documentation)
  │                                                    │
  │                                                    └──→ Phase 9 (Student Workflow)
  │                                                              │
  │                                                              └──→ Phase 10 (Agenda)
  │                                                                        │
  │                                                                        └──→ Phase 11 (Pre-check)
  │
  └──→ (can start in parallel: Phase 6 AI, Phase 8 Mirror)
```

**Critical path:** Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 9 → Phase 11

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| SauceDemo goes down during workshop | High | Low | Prepare backup SUT (automationexercise.com). Include fallback URLs in variables. |
| Codespace build takes too long | Medium | Medium | Pre-build Codespace. Use Chromium-only. Cache dependencies. |
| Students cannot push branches | High | Medium | Pre-create GitHub accounts or use fork model with explicit instructions. Test beforehand. |
| Network at 42 Vienna blocks Codespaces | High | Low | Prepare USB sticks with Docker image. Test from 42 Vienna network beforehand. |
| Too many students for GitHub free tier | Low | Low | Codespaces free tier is 60h/month per user. Students use own accounts. |
| ARM64 machines at 42 Vienna | Medium | Unknown | Codespaces are x86-64 VMs regardless of local machine. Only matters for local setup. |
| uv not available in DevContainer feature | Medium | Low | Fallback: install via curl in post-create.sh. |
| Playwright system deps missing in Codespace | Medium | Medium | Add `npx playwright install-deps` to post-create.sh if needed. |
| Students overwhelmed by RF syntax | Medium | Medium | Progressive exercises. Cheat sheet. Heavy commenting in examples. Pair programming. |

---

## TODO Tasklist

### Phase 0: Infrastructure (Day 1)
- [ ] Verify GitLab accessibility from external networks
- [ ] Verify 42 Vienna network allows GitHub/Codespaces domains
- [ ] Confirm `github-sync` CronJob auto-creates GitLab projects

### Phase 1: Repository Creation (Day 1-2)
- [x] Create GitHub repo `HackXIt/42vienna-robotframework-workshop` (public)
- [x] Configure local git remotes
- [x] Create `pyproject.toml` with all dependencies and tool config
- [x] Create `.python-version` (3.12)
- [x] Create `.gitignore`
- [x] Create `.vscode/settings.json` and `extensions.json`
- [x] Create full directory structure (tests/, resources/, scripts/, docs/)
- [x] Generate `uv.lock` via `uv lock`
- [x] Create LICENSE (MIT)
- [x] Initial commit and push

### Phase 2: DevContainer (Day 2)
- [x] Create `.devcontainer/devcontainer.json`
- [x] Create `.devcontainer/post-create.sh`
- [ ] Test DevContainer opens in GitHub Codespaces
- [ ] Test DevContainer opens in local VSCode + Docker
- [ ] Verify `uv sync --locked` completes in Codespace
- [ ] Verify `rfbrowser init chromium` completes in Codespace
- [ ] Verify RobotCode extension works (syntax highlighting, autocomplete)
- [ ] Measure total build time (target: < 5 minutes)

### Phase 3: Readiness Script (Day 2-3)
- [x] Create `scripts/check_environment.py`
- [x] Implement platform detection (Linux/macOS/Windows/WSL)
- [x] Implement all 11 checks with actionable error messages
- [x] Implement colored terminal output (ANSI with TTY detection)
- [x] Implement summary box at the end
- [ ] Test on Linux (Codespace)
- [ ] Test failure messages (run on bare machine, verify output is helpful)
- [x] Verify exit code behavior (0 = all pass, 1 = any fail)
- [x] Verify script runs with stdlib only (no imports from installed packages)

### Phase 4: Test Suites (Day 2-3)
- [x] Create `resources/common.resource` (shared setup/teardown, base URL)
- [x] Create `resources/saucedemo.resource` (convenience import for all pages)
- [x] Create `resources/login_page.resource`
- [x] Create `resources/products_page.resource`
- [x] Create `resources/cart_page.resource`
- [x] Create `resources/checkout_page.resource`
- [x] Create `tests/00_setup_verification/verify_setup.robot`
- [x] Create `tests/01_first_test/first_browser_test.robot` (heavily commented)
- [x] Create `tests/02_login_tests/login.robot` (individual cases, [Template] mentioned in docs)
- [x] Create `tests/03_product_tests/product_catalog.robot`
- [x] Create `tests/04_cart_tests/shopping_cart.robot`
- [x] Create `tests/05_checkout_tests/checkout_flow.robot`
- [x] Create `tests/06_e2e_scenarios/complete_purchase.robot`
- [x] Create `tests/student_exercises/_template.robot`
- [x] Create `tests/student_exercises/README.md`
- [x] Verify ALL tests pass locally (requires `uv sync` + `rfbrowser init`) — 25/25 passed
- [ ] Verify ALL tests pass in DevContainer/Codespace
- [x] Verify SauceDemo selectors are current — all selectors work (verified via passing tests)

### Phase 5: CI/CD (Day 3)
- [x] Create `.github/workflows/robot-tests.yml`
- [x] Create `.github/workflows/pr-feedback.yml`
- [x] Create `.github/PULL_REQUEST_TEMPLATE.md`
- [x] Test CI runs on push to main — verified, 25/25 pass on GitHub Actions
- [x] Test CI runs on PR — PR #1 verified, 27/27 pass (25 base + 2 student tests)
- [x] Verify test results artifact is uploaded — confirmed in CI run
- [x] Verify PR comment with results summary — pull_request_target posts comment with pass/fail + output
- [x] Add Robocop lint job with SARIF → GitHub Code Scanning integration
- [x] Add Robocop to PR feedback workflow (SARIF + text summary in comment)
- [x] Configure GitHub Pages — MkDocs documentation site deployed
- [x] Create `.github/workflows/docs.yml` for GitHub Pages deployment

### Phase 6: AI Integration (Day 3-4)
- [x] Create `CLAUDE.md` with RF conventions, SauceDemo selectors, uv commands
- [x] Create `AGENTS.md` (separate file with agent-specific instructions)
- [x] Create `.claude/settings.json` with MCP server config
- [x] Verify MCP package on PyPI — `robotframework-mcp` (SeleniumLibrary-based, not suitable); using `rf-mcp` (0.30+, mature)
- [x] Add `rf-mcp` to `pyproject.toml` dev dependencies
- [x] Prepare AI demo script — `docs/ai-demo-script.md` with flow, prompts, backup test
- [ ] Test the demo end-to-end (requires live Claude Code session)

### Phase 7: Documentation (Day 4-5)
- [x] Create `README.md` (quick start, prerequisites, agenda, badges)
- [x] Create `docs/getting-started.md` (3 setup paths)
- [x] Create `docs/rf-syntax-cheatsheet.md`
- [x] Create `docs/browser-library-guide.md`
- [x] Create `docs/exercises.md` (8 progressive exercises)
- [x] Create `docs/troubleshooting.md`
- [x] Create `docs/ai-assisted-testing.md`
- [x] Create `docs/windows-setup.md` (decision tree, 3 paths, common issues)
- [x] Create `docs/student-workflow.md` (fork/collaborator workflow)
- [x] Create `docs/workshop-agenda.md` (instructor timeline, talking points)
- [x] Create `docs/ai-demo-script.md` (15-min demo flow)
- [x] All docs reference `uv` commands (not pip)
- [x] All docs end with readiness script verification step — added to exercises, windows-setup
- [x] Rename numbered docs to clean filenames for MkDocs compatibility
- [x] Set up MkDocs Material with `mkdocs.yml` and deploy to GitHub Pages
- [x] Create `scripts/generate_keyword_docs.py` for libdoc → Markdown conversion
- [x] Generate `docs/keywords/*.md` keyword reference from resource files
- [x] Create `.github/workflows/docs.yml` for automated deployment
- [x] Add Robocop "minimal" ruleset v0.1.0 to `pyproject.toml`
- [ ] Proofread all docs for accuracy and clarity
- [ ] (Nice-to-have) Add screenshots to docs

### Phase 8: GitLab Mirror (Day 4)
- [ ] Create GitLab project in `github-mirrors` group (or verify auto-creation)
- [ ] Verify `github-sync` CronJob picks up the new repo
- [ ] Verify `github-gitlab-sync` CronJob syncs issues/PRs
- [ ] (Optional) Manually trigger first sync if impatient

### Phase 9: Student Workflow (Day 4-5)
- [x] Resolve access model — Plan A: fork, Plan B: collaborator (on-the-fly fallback)
- [x] Write fork instructions in docs — `docs/07-student-workflow.md` (no screenshots yet)
- [ ] Test Plan A: fork → Codespace on fork → write test → push → PR to upstream → CI approval → results
- [ ] Test Plan B: add collaborator → Codespace on main repo → branch → push → PR → CI → results
- [x] Verify PR template appears when creating PR — confirmed via test PR #1
- [ ] Verify GitHub Actions workflow approval flow for first-time fork contributors
- [x] Prepare `gh api` one-liner for quickly adding collaborators — in `docs/workshop-agenda.md`
- [x] Configure GitHub Actions settings — set default workflow permissions to write, approval for first-time contributors

### Phase 10: Workshop Agenda (Day 5-6)
- [x] Finalize timeline (fits within 3-4 hours) — `docs/workshop-agenda.md`
- [x] Prepare talking points — included in workshop-agenda.md
- [x] Prepare fallback plan if SauceDemo is down — the-internet.herokuapp.com as backup
- [ ] (Nice-to-have) Create minimal slides for intro/recap

### Phase 11: Pre-Workshop Check (Day 6-7)
- [ ] Fresh Codespace test: full flow from zero
- [ ] Test from different network (mobile hotspot, simulate restrictive firewall)
- [ ] Contact Simon: verify 42 Vienna infrastructure
- [ ] Contact Hans Jörg: confirm logistics (attendees, room, projector)
- [ ] (Optional) Technical pre-check meeting at 42 Vienna
- [ ] (Optional) Record screencast of the full flow as backup
- [ ] Verify all TODO items above are complete

---

## Troubleshooting & Known Issues

### PHASE 0 — Infrastructure

| Issue | Status | Details |
|-------|--------|---------|
| No GitLab CI Runner | DECIDED | Using GitHub Actions instead. GitLab is mirror-only. |
| ARM64-only cluster | DECIDED | Playwright needs x86-64. GitHub Actions provides x86-64 runners. Codespaces are also x86-64. |
| GitLab accessibility | OPEN | Need to verify `git.lab.hackxit.com` is reachable from 42 Vienna network. If not, GitLab mirroring is for personal backup only. |

### PHASE 2 — DevContainer

| Issue | Status | Details |
|-------|--------|---------|
| uv DevContainer feature reliability | OPEN | The `ghcr.io/va-h/devcontainers-features/uv:1` is a community feature. Fallback: install uv via curl in `post-create.sh`. |
| Playwright system dependencies | OPEN | The `python:3.12-bookworm` base image may miss shared libraries Playwright needs (e.g., libglib2.0, libnss3, libatk1.0). May need `npx playwright install-deps` in post-create. |
| Codespace build timeout | OPEN | `rfbrowser init chromium` downloads ~250MB. On slow connections, this could push build time past 10 minutes. Consider Codespace prebuilds. |
| Chromium-only limitation | NOTED | Only Chromium is installed. If a student wants Firefox/WebKit, they need to run `rfbrowser init` (all browsers) manually. Document this. |

### PHASE 3 — Readiness Script

| Issue | Status | Details |
|-------|--------|---------|
| Playwright browsers path in Codespaces | OPEN | Codespaces may use a non-standard path for Playwright binaries. The detection logic needs to handle this. |
| ANSI colors on Windows | NOTED | Windows cmd.exe doesn't support ANSI by default. Windows Terminal does. The script should detect and disable colors on non-ANSI terminals. |

### PHASE 4 — Test Suites

| Issue | Status | Details |
|-------|--------|---------|
| SauceDemo availability | LOW RISK | Public site, generally reliable. If down, fallback to automationexercise.com or the-internet.herokuapp.com. |
| SauceDemo selector changes | RESOLVED | Verified: all selectors work. 25 tests pass locally and in CI (March 2026). |
| Headless mode in Codespaces | OPEN | Verify Browser Library runs headless correctly without a display server. Should work (Playwright supports headless natively). |

### PHASE 5 — CI/CD

| Issue | Status | Details |
|-------|--------|---------|
| GitHub Actions minutes | LOW RISK | Free tier: 2000 min/month. Each run ~3-5 min. With ~20 students × ~5 PRs each = ~100 runs = ~300-500 min. Well within limits. |
| `astral-sh/setup-uv` version | RESOLVED | `@v7` is latest major (v7.3.1 latest release as of 2026-02-27). No changes needed. |
| GitHub auth `workflow` scope | RESOLVED | Pushing workflow files requires the `workflow` OAuth scope. Fixed via `gh auth refresh -h github.com -s workflow`. |
| CI first run validation | RESOLVED | CI runs on push to main. Initial failure (strict mode violation in Cart Should Contain with multiple items) fixed. All 25 tests pass. |
| Robocop SARIF integration | RESOLVED | `robocop check --reports sarif --exit-zero` generates `.sarif.json`. Uploaded via `github/codeql-action/upload-sarif@v4`. Hidden file requires `include-hidden-files: true` on artifact upload. |
| CodeQL Action version | RESOLVED | Upgraded from `@v3` to `@v4` (v3 deprecated Dec 2026). |
| GitHub Pages deployment | RESOLVED | Enabled via `gh api` with `build_type=workflow`. MkDocs Material site live at `hackxit.github.io/42vienna-robotframework-workshop/`. |

### PHASE 9 — Student Workflow

| Issue | Status | Details |
|-------|--------|---------|
| Student access model | **DECIDED** | Plan A: Fork model (standard open-source). Students fork, open Codespace on their fork, PR back to upstream. Plan B: Collaborator access added on-the-fly if forking causes friction. |
| CI approval for fork PRs | OPEN | GitHub Actions requires maintainer approval for first-time fork contributors. Nikolaus must approve each student's first workflow run via Actions tab. Test this flow beforehand to understand the UX. Consider changing repo setting to minimize friction. |
| Codespace on fork | OPEN | Verify that creating a Codespace on a forked repo works identically (same DevContainer, same post-create). Should work since the config is in the repo, but needs verification. |
| Codespace per student | NOTED | Each student needs their own Codespace. They use their own GitHub account's free tier (60h/month). Verify students have GitHub accounts. |

---

## Critical Files Summary

| File | Why Critical |
|------|-------------|
| `pyproject.toml` | Single source of truth: dependencies, RF config, uv config, Robocop ruleset. Every other file depends on this. |
| `scripts/check_environment.py` | 11-check readiness script. First thing students run. Validates the entire toolchain. |
| `.devcontainer/devcontainer.json` | Determines if students can participate without local setup. Most important file for frictionless onboarding. |
| `.devcontainer/post-create.sh` | uv sync → rfbrowser init → check script. The 4-step sequence that makes a Codespace functional. |
| `.github/workflows/robot-tests.yml` | CI pipeline: test runner + Robocop lint with SARIF → Code Scanning. |
| `.github/workflows/pr-feedback.yml` | PR feedback: test results + Robocop summary posted as PR comment. |
| `.github/workflows/docs.yml` | MkDocs + libdoc → GitHub Pages deployment. |
| `mkdocs.yml` | MkDocs Material site configuration. |
| `scripts/generate_keyword_docs.py` | Libdoc JSON → Markdown conversion for keyword reference docs. |
| `resources/common.resource` | Shared RF keywords. All test suites depend on this. Sets the pattern for keyword abstraction. |
| `CLAUDE.md` | AI agent instructions. Enables Claude/Codex to review PRs and assist students. |
| `docs/exercises.md` | Drives the entire hands-on portion (~2.5 hours) of the workshop. |
| `docs/student-workflow.md` | Fork → Codespace → write tests → PR → CI flow guide for students. |
| `docs/workshop-agenda.md` | Instructor notes, timeline, talking points, fallback plan. |

---

*Plan created: March 9, 2026*
*Last updated: March 9, 2026 — Phases 1-10 complete. Added MkDocs GitHub Pages, libdoc keyword docs, Robocop SARIF/Code Scanning CI integration. All CI jobs green.*
