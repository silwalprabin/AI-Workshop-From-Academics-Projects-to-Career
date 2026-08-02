# Installation Guide

Everything you need for the workshop, per operating system. **All downloads come from official sites only.** Do not download these tools from third-party mirrors or "free download" pages.

> **Do the pre-work.** Install everything and pull one chat model + one embedding model **before** the workshop so you're not downloading gigabytes on shared Wi-Fi.

---

## Hardware requirements

| Resource | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| RAM | 8 GB | 16 GB+ | LLMs are memory-hungry; more RAM = larger models. |
| Disk (free) | 15 GB | 30 GB+ | Models are 1–8 GB each; Docker images add up. |
| CPU | 4 cores (x86-64 / Apple Silicon) | 8+ cores | Modern CPU handles small quantized models fine. |
| GPU | Optional | NVIDIA (CUDA) or Apple Silicon | Optional but speeds up generation a lot. |
| OS | Win 10/11 64-bit, macOS 12+, Ubuntu 20.04+ | Latest stable | 64-bit only. |

**Model sizing rule of thumb:** on 8 GB RAM, stick to ~3B-parameter quantized models. With 16 GB you can run ~7–8B comfortably. If a model is slow or the machine swaps, pick a smaller model.

---

## Tool overview

| Tool | What it is | Why we need it |
|------|-----------|----------------|
| Python 3.12+ | Programming language & runtime | Both projects are written in Python. |
| Git | Version control | Clone starter code; track and push your work. |
| VS Code | Code editor | Write and debug code with extensions. |
| Ollama | Local LLM runtime | Run open-source chat & embedding models offline. |
| Docker | Containerization | Package apps to run anywhere. |
| pip / uv + venv | Package & env management | Isolated, reproducible dependencies. |

---

# Windows

## 1. Python 3.12+
- **Official download:** https://www.python.org/downloads/windows/
- **Steps:**
  1. Download the latest **Python 3.12.x** Windows installer (64-bit).
  2. Run it and **check "Add python.exe to PATH"** on the first screen (critical).
  3. Click **Install Now**; then **Disable path length limit** if offered.
- **Verify:** open a **new** PowerShell and run:
  ```powershell
  python --version
  pip --version
  ```
- **Common errors:**
  - *`python` opens Microsoft Store:* disable the Store alias in **Settings → Apps → Advanced app settings → App execution aliases** (turn off the `python.exe` aliases), or reinstall with "Add to PATH".
  - *`pip` not recognized:* use `python -m pip ...`, or reinstall with PATH enabled.

## 2. Git
- **Official download:** https://git-scm.com/download/win
- **Steps:** run the installer; accept defaults (VS Code as editor is a fine choice; keep "Git from the command line and 3rd-party software").
- **Verify:**
  ```powershell
  git --version
  ```
- **Common errors:** *`git` not recognized* → reopen the terminal (PATH updates need a new session).

## 3. VS Code
- **Official download:** https://code.visualstudio.com/docs/setup/windows
- **Steps:** install, then add the **Python** extension from the Extensions panel.
- **Verify:** `code --version` (or launch the app).

## 4. Ollama
- **Official download:** https://ollama.com/download/windows
- **Steps:** run `OllamaSetup.exe`; it installs a background service listening on `http://localhost:11434`.
- **Verify:**
  ```powershell
  ollama --version
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text
  ollama run llama3.2:3b "Say hello in one sentence."
  ```
- **Common errors:**
  - *Connection refused:* ensure the Ollama app/service is running (check the system tray).
  - *Slow first response:* the model loads into memory on first call — subsequent calls are faster.

## 5. Docker (Optional)
- **Official download:** https://docs.docker.com/desktop/install/windows-install/
- **Steps:**
  1. Install **Docker Desktop**; enable the **WSL 2** backend when prompted.
  2. If WSL 2 is missing, follow Docker's linked instructions (or run `wsl --install` in an admin PowerShell) and reboot.
- **Verify:**
  ```powershell
  docker --version
  docker run hello-world
  ```
- **Common errors:** *"Docker daemon is not running"* → start Docker Desktop and wait for the whale icon to go steady.

## 6. venv + packages
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- **Common error — activation blocked:** if you see *"running scripts is disabled on this system"*, run once:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
  Then re-run the activate command. (Alternatively use `cmd.exe` and `\.venv\Scripts\activate.bat`.)

### Optional: uv (fast installer)
- **Docs:** https://docs.astral.sh/uv/getting-started/installation/
  ```powershell
  uv venv
  uv pip install -r requirements.txt
  ```

---

# macOS

## 1. Python 3.12+
- **Official download:** https://www.python.org/downloads/macos/
- **Steps:** download the **macOS 64-bit universal2** installer for Python 3.12.x and run it.
- **Verify:**
  ```bash
  python3 --version
  pip3 --version
  ```
- **Note:** macOS's built-in `python3` may be older; the python.org installer gives you 3.12. Use `python3`/`pip3` on macOS.

## 2. Git
- **Official download:** https://git-scm.com/download/mac
- **Steps:** the simplest path is to run `git --version` once — macOS offers to install the Command Line Developer Tools. Or install from the link above.
- **Verify:** `git --version`

## 3. VS Code
- **Official download:** https://code.visualstudio.com/docs/setup/mac
- **Steps:** unzip, drag **Visual Studio Code** to **Applications**. Optionally run **"Shell Command: Install 'code' command in PATH"** from the Command Palette.
- **Verify:** `code --version` (or launch the app). Add the **Python** extension.

## 4. Ollama
- **Official download:** https://ollama.com/download/mac
- **Steps:** open the downloaded `.dmg`, move Ollama to Applications, and launch it (menu-bar icon). It serves on `http://localhost:11434`.
- **Verify:**
  ```bash
  ollama --version
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text
  ollama run llama3.2:3b "Say hello in one sentence."
  ```
- **Note (Apple Silicon):** models use the GPU automatically — expect good speed on M-series chips.

## 5. Docker
- **Official download:** https://docs.docker.com/desktop/install/mac-install/
- **Steps:** download the `.dmg` matching your chip (**Apple Silicon** or **Intel**), install, and launch Docker Desktop.
- **Verify:**
  ```bash
  docker --version
  docker run hello-world
  ```

## 6. venv + packages
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Optional: uv
- **Docs:** https://docs.astral.sh/uv/getting-started/installation/

---

# Ubuntu / Linux

## 1. Python 3.12+
- **Official reference:** https://www.python.org/downloads/source/ (source) and https://docs.python.org/3/using/unix.html
- **Steps (Ubuntu 22.04+):**
  ```bash
  sudo apt update
  sudo apt install -y python3 python3-venv python3-pip
  ```
  If your distro's `python3` is below 3.12, use the official deadsnakes route documented for your Ubuntu version, or build from the python.org source link above.
- **Verify:**
  ```bash
  python3 --version
  pip3 --version
  ```

## 2. Git
- **Official download:** https://git-scm.com/download/linux
  ```bash
  sudo apt update && sudo apt install -y git
  ```
- **Verify:** `git --version`

## 3. VS Code
- **Official download:** https://code.visualstudio.com/docs/setup/linux
- **Steps:** install the `.deb` from the link, or follow the official APT repository instructions on that page.
- **Verify:** `code --version`. Add the **Python** extension.

## 4. Ollama
- **Official download:** https://ollama.com/download/linux
- **Steps:** follow the official install command shown on that page:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```
- **Verify:**
  ```bash
  ollama --version
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text
  ollama run llama3.2:3b "Say hello in one sentence."
  ```
- **Note:** for NVIDIA GPU acceleration, install your distro's CUDA drivers; Ollama detects them automatically.

## 5. Docker
- **Official download:** https://docs.docker.com/engine/install/ubuntu/
- **Steps:** follow the official "Install using the apt repository" instructions on that page. Then add yourself to the docker group so you don't need `sudo`:
  ```bash
  sudo usermod -aG docker $USER
  # log out and back in for this to take effect
  ```
- **Verify:**
  ```bash
  docker --version
  docker run hello-world
  ```

## 6. venv + packages
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Optional: uv
- **Docs:** https://docs.astral.sh/uv/getting-started/installation/

---

## Post-install checklist

Run these; all should succeed before the workshop:

```bash
python --version        # or python3 on macOS/Linux  -> 3.12.x
pip --version           # or pip3
git --version
docker run hello-world
ollama list             # shows llama3.2:3b and nomic-embed-text
```

If any command fails, see `TROUBLESHOOTING.md` (Top 30 errors) or ask a facilitator during the Prerequisites section.
