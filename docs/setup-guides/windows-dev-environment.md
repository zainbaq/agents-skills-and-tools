# Windows Development Environment Setup for AI Engineering

A practical setup guide for an AI engineering development environment on Windows 11, covering WSL2, Python, Azure CLI, Docker, and Claude Code. Written from the perspective of someone building Python Azure Functions, RAG pipelines, and containerized Flask apps.

## Prerequisites

| Component | Version | Notes |
|-----------|---------|-------|
| Windows 11 | 22H2 or later | Required for WSL2 reliability |
| WSL2 (Ubuntu 22.04 LTS) | Latest | Strongly preferred over working directly in PowerShell |
| Python | 3.11 or 3.12 | Avoid 3.13 — PyO3-dependent packages (pydantic v2, cryptography) lag behind |
| Docker Desktop | Latest | Requires WSL2 backend; 4GB RAM minimum |
| Azure CLI | Latest | Install inside WSL2, not Windows |
| Node.js | 20 LTS | Required for Claude Code and Power Platform CLI |
| Git | Latest | Configure inside WSL2 |

---

## Step 1: Install WSL2 and Ubuntu

Open PowerShell as Administrator:

```powershell
wsl --install -d Ubuntu-22.04
```

Restart when prompted. On first launch, create a Linux username and password.

Update packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl git unzip
```

**Why WSL2 and not PowerShell**: Python package compilation (native extensions like `pydantic-core`, `cryptography`, `pyarrow`) is significantly more reliable on Linux. Azure CLI behaves as documented. Docker Desktop's WSL2 backend provides better file system performance than the Hyper-V backend.

---

## Step 2: Python Environment

**Install Python 3.12** (not the Ubuntu default 3.10):

```bash
sudo apt install -y python3.12 python3.12-venv python3.12-dev python3-pip
```

Verify:
```bash
python3.12 --version  # Python 3.12.x
```

For managing multiple Python versions (recommended if working on projects with different version requirements):

```bash
# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install and set Python 3.12
pyenv install 3.12.3
pyenv global 3.12.3
```

**Per-project virtual environments**:

```bash
cd /path/to/project
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### The PyO3 / pydantic-core Version Compatibility Problem

If you see errors like `cannot import name 'ModelMetaclass' from 'pydantic'` or `mismatch between Python version and PyO3 compiled version`, the issue is a compiled C extension (pydantic-core, cryptography, etc.) that was compiled for a different Python minor version.

The fix is always the same: delete `.venv`, re-create it with the exact Python version the package was compiled for, and reinstall.

```bash
rm -rf .venv
python3.12 -m venv .venv  # must match the version the wheel was built for
source .venv/bin/activate
pip install --no-cache-dir -r requirements.txt
```

If the issue persists, force a build from source:
```bash
pip install --no-binary :all: pydantic-core
```

---

## Step 3: Azure CLI

Install inside WSL2 (not the Windows installer — they are separate installations and the Windows one does not work in WSL2 without PATH gymnastics):

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
az --version
```

Authenticate:
```bash
az login
```

This opens a browser on the **Windows** side automatically from WSL2. If it doesn't (headless environment), use:

```bash
az login --use-device-code
```

Set your default subscription:
```bash
az account set --subscription "Your Subscription Name"
```

### Assign Developer RBAC Roles

For local development against Azure AI Search and Azure OpenAI, your developer account needs the same roles the managed identity has in production:

```bash
# Get your user object ID
USER_ID=$(az ad signed-in-user show --query id -o tsv)

# Azure AI Search — dev instance
az role assignment create \
  --role "Search Index Data Contributor" \
  --assignee-object-id $USER_ID \
  --assignee-principal-type User \
  --scope /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Search/searchServices/{name}

# Azure OpenAI — dev instance
az role assignment create \
  --role "Cognitive Services OpenAI User" \
  --assignee-object-id $USER_ID \
  --assignee-principal-type User \
  --scope /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{name}
```

With these roles assigned and `az login` completed, `DefaultAzureCredential` in your Python code works locally without any additional configuration.

---

## Step 4: Environment Variables

Never hardcode Azure endpoints, index names, or deployment IDs. Use a `.env` file for local development.

```bash
cp .env.example .env
```

`.env` structure for a typical RAG project:

```bash
# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_INDEX=docs-dev
AZURE_SEARCH_SEMANTIC_CONFIG=semantic-config

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-openai-resource.openai.azure.com
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o

# Azure Storage
AZURE_STORAGE_ACCOUNT=yourstorageaccount
AZURE_STORAGE_CONTAINER=documents-dev

# Application
LOG_LEVEL=DEBUG
ENVIRONMENT=development
```

**Do NOT set `AZURE_CLIENT_SECRET` locally.** That variable is for CI/CD pipelines and service-to-service authentication that cannot use managed identity. Setting it locally overrides `DefaultAzureCredential`'s managed identity path and makes local behavior diverge from production.

Load with [python-dotenv](https://pypi.org/project/python-dotenv/):
```python
from dotenv import load_dotenv
load_dotenv(".env")
```

---

## Step 5: Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. During installation, select **Use WSL2 instead of Hyper-V** (default on Windows 11)
3. After installation, in Docker Desktop Settings → Resources → WSL Integration, enable integration for Ubuntu-22.04

Verify from inside WSL2:
```bash
docker --version
docker compose version
```

Test a build:
```bash
docker compose up --build
```

**If Docker can't access files in WSL2**: Check that WSL Integration is enabled for your Ubuntu distro in Docker Desktop settings. This is the most common setup issue.

**Memory limits**: Docker Desktop defaults to 50% of system RAM. For large Azure Function images or multi-container RAG pipelines, increase this in Settings → Resources.

---

## Step 6: Node.js (for Claude Code and Power Platform CLI)

```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# Install Node 20 LTS
nvm install 20
nvm use 20
node --version  # v20.x.x
```

Install Claude Code:
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Install Power Platform CLI:
```bash
npm install -g @microsoft/powerplatform-cli
pac --version
```

---

## Step 7: Install Claude Code Sub-Agents from This Repo

```bash
# Clone this repo
git clone https://github.com/zainbaq/agents-skills-and-tools.git
cd agents-skills-and-tools

# Install sub-agents globally (available in all Claude Code projects)
mkdir -p ~/.claude/agents
cp agents/architect/architect.md ~/.claude/agents/
cp agents/code-reviewer/code-reviewer.md ~/.claude/agents/
cp agents/security-auditor/security-auditor.md ~/.claude/agents/
cp agents/integration-validator/integration-validator.md ~/.claude/agents/
cp agents/qa-engineer/qa-engineer.md ~/.claude/agents/

# Install skills globally
mkdir -p ~/.claude/skills
cp skills/implementation-planning/SKILL.md ~/.claude/skills/implementation-planning.md
cp skills/adr-writing/SKILL.md ~/.claude/skills/adr-writing.md
cp skills/api-design/SKILL.md ~/.claude/skills/api-design.md
```

Restart Claude Code after copying files. Verify sub-agents are available with `/agents` inside a Claude Code session.

---

## Step 8: Git Configuration

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global core.editor "code --wait"  # VS Code as default editor

# Generate SSH key for GitHub
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
# Add this public key to GitHub Settings → SSH keys
```

Test the connection:
```bash
ssh -T git@github.com
# Hi username! You've successfully authenticated...
```

**SSH from VS Code Remote WSL**: VS Code's Remote WSL extension forwards your WSL2 SSH agent. If SSH works in WSL2 terminal but not in VS Code's integrated terminal, run `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519` and add it to your `~/.bashrc`.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `az login` opens nothing in WSL2 | Browser not found by xdg-open | Use `az login --use-device-code` |
| `DefaultAzureCredential` fails locally | Not logged in via Azure CLI | Run `az login` and confirm correct subscription with `az account show` |
| `pydantic` import error after pip install | pydantic-core compiled for wrong Python version | Delete `.venv`, recreate with the exact correct Python version, reinstall |
| Docker not found inside WSL2 | WSL integration not enabled | Enable in Docker Desktop Settings → Resources → WSL Integration |
| `docker compose` works but files not synced | WSL2 drive mount permissions | Access project files via WSL2 path (`/home/user/...`), not Windows path (`/mnt/c/...`) |
| Claude Code sub-agents not showing | Files not reloaded | Restart Claude Code after copying `.md` files to `.claude/agents/` |
| `pac` not found after npm install | Node binary path not in shell PATH | Run `source ~/.bashrc` or open a new terminal |
| SSH works in terminal but not VS Code | SSH agent not running in VS Code shell | Add `eval "$(ssh-agent -s)" && ssh-add` to `~/.bashrc` |
