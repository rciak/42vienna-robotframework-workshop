# Setup

## Selected history

```bash
git clone git@github.com:rciak/42vienna-robotframework-workshop.git
cd 42vienna-robotframework-workshop
python --version
sudo apt-get install python3
sudo apt install curl

curl -LsSf https://astral.sh/uv/install.sh | sh
uv run rfbrowser install --help
sudo apt install npm
uv run rfbrowser install --with-deps chromium
uv run rfbrowser init --with-deps chromium
uv run robot tests/00_setup_verification

code .
source /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/activate
```

Unsure: Seems not to work; Did History not got saved properly?!
```bash
CLEAR cd /home/rene/WORKSHOP/42vienna-robotframework-workshop ; /usr/bin/env /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python /home/rene/.vscode/extensions/d-biehl.robotcode-0.82.3/bundled/tool/robotcode --default-path . debug --no-debug -- -d results -P /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python --parse-include tests/01_first_test/first_browser_test.robot --name 42Vienna-Robotframework-Workshop --suite 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test --by-longname 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test 
 CLEAR cd /home/rene/WORKSHOP/42vienna-robotframework-workshop ; /usr/bin/env /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python /home/rene/.vscode/extensions/d-biehl.robotcode-0.82.3/bundled/tool/robotcode --default-path . debug --no-debug -- -d results -P /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python --parse-include tests/01_first_test/first_browser_test.robot --name 42Vienna-Robotframework-Workshop --suite 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test --by-longname 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test 
```

## VS Code Plugin

* RobotCode - Robot Framework Support  
v0.82.3  
Daniel Biehl  
robotcode.io

## Full history

Just for backup, if something above would turn out incomplete.

```bash
git clone git@github.com:rciak/42vienna-robotframework-workshop.git
 ls
 cd 42vienna-robotframework-workshop
 ls
 cd docs
 ls
 cd ..
 ls
 uv run robot tests/00_setup_verification/
 phython --version
 python --version
 sudo apt-get install python
 sudo apt-get install python3
 curl -LsSf https://astral.sh/uv/install.sh | sh
 sudo apt install curl
 curl -LsSf https://astral.sh/uv/install.sh | sh
 uv sync
 uv run rfbrowser init chromium
 uv run rfbrowser init --with-deps chromium
 uv run rfbrowser --help
 uv run rfbrowser install --help
 uv run rfbrowser install --with-deps
 uv run rfbrowser install --help
 uv run rfbrowser install --with-deps chromium
 sudo apt install npm
 uv run rfbrowser install --with-deps chromium
 uv run rfbrowser init --with-deps chromium
 uv run tests/00_setup_verification
 uv run robot tests/00_setup_verification
 code .
 source /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/activate
 clear
 cleR
 CLEAR
 clear
 clear cd /home/rene/WORKSHOP/42vienna-robotframework-workshop ; /usr/bin/env /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python /home/rene/.vscode/extensions/d-biehl.robotcode-0.82.3/bundled/tool/robotcode --default-path . debug --no-debug -- -d results -P /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python --parse-include tests/01_first_test/first_browser_test.robot --name 42Vienna-Robotframework-Workshop --suite 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test --by-longname 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test 
 CLEAR cd /home/rene/WORKSHOP/42vienna-robotframework-workshop ; /usr/bin/env /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python /home/rene/.vscode/extensions/d-biehl.robotcode-0.82.3/bundled/tool/robotcode --default-path . debug --no-debug -- -d results -P /home/rene/WORKSHOP/42vienna-robotframework-workshop/.venv/bin/python --parse-include tests/01_first_test/first_browser_test.robot --name 42Vienna-Robotframework-Workshop --suite 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test --by-longname 42Vienna-Robotframework-Workshop.Tests.01\ First\ Test.First\ Browser\ Test 
```