# Getting Started

Choose your setup method. **Codespaces is recommended** — it works in your browser, no local installation needed.

## Option 1: GitHub Codespaces (Recommended)

1. Go to [the repository on GitHub](https://github.com/HackXIt/42vienna-robotframework-workshop)
2. Click **"Fork"** (top right) → Click **"Create fork"**
3. On **your fork**, click **"Code"** → **"Codespaces"** → **"Create codespace on main"**
4. Wait for the DevContainer to build (~3-5 minutes the first time)
5. When the terminal appears, run:
   ```bash
   uv run robot tests/00_setup_verification/
   ```
6. If you see `1 test, 1 passed` — you're ready!

### What happens during setup?

The DevContainer automatically:
- Installs Python 3.12 and Node.js 22
- Installs `uv` (our package manager)
- Runs `uv sync --locked` (installs Robot Framework, Browser Library, etc.)
- Runs `rfbrowser init chromium` (downloads Chromium browser, ~250MB)
- Runs the environment check script

## Option 2: Local VSCode + Docker (DevContainer)

If you prefer running locally:

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Install [VS Code](https://code.visualstudio.com/)
3. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
4. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop.git
   ```
5. Open in VS Code → Click **"Reopen in Container"** when prompted
6. Wait for the build to complete
7. Run:
   ```bash
   uv run robot tests/00_setup_verification/
   ```

## Option 3: Local Without Docker

For native setup (Linux/macOS/WSL):

1. Install Python 3.12+: https://www.python.org/downloads/
2. Install Node.js 22+: https://nodejs.org/
3. Install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
4. Clone and set up:
   ```bash
   git clone https://github.com/YOUR_USERNAME/42vienna-robotframework-workshop.git
   cd 42vienna-robotframework-workshop
   uv sync
   uv run rfbrowser init chromium
   ```
5. Verify:
   ```bash
   python scripts/check_environment.py
   uv run robot tests/00_setup_verification/
   ```

For Windows-specific instructions, see [Windows Setup](windows-setup.md).

## Verify Your Setup

Regardless of your setup method, run the environment check:

```bash
python scripts/check_environment.py
```

This checks all 11 prerequisites and shows actionable fix instructions for any issues.
