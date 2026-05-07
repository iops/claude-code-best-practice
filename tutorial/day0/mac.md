# macOS Setup

[Back to Day 0](README.md)

---
**Step 1: Download VS Code**
go to:

https://code.visualstudio.com

The site auto-detects they're on a Mac and shows a big blue "Download for macOS" button. Click it.

It'll download a .zip file (something like VSCode-darwin-universal.zip) to their Downloads folder.

**Step 2: Install it**

doubleclick the file you just downloaded 

Drag the "Visual Studio Code" app into the Applications folder

**Step 3: Open it for the first time**

Open Launchpad or open Applications in Finder
Click Visual Studio Code
macOS will show a warning: "Visual Studio Code is an app downloaded from the internet. Are you sure you want to open it?" — click Open
This warning only appears the first time.

**Step 4: Pin it to the Dock (optional but helpful)**
Once VS Code is open, right-click its icon in the Dock → Options → Keep in Dock. Now they can launch it with one click going forward.

## Install claude cli
**Verify**
- Check if claude is already installed:
- ```bash
  claude --version
  which claude
  ```
- if installed 
  ```bash
  claude doctor
  ```
- follow instructions to fix any issues

- if not installed, follow the instructions below to install it.

**Terminal**
- Open Terminal (press `Cmd + Space`, type "Terminal", hit Enter)

**Install:**
  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```

**Edit the config so that you get stable updates instead of beta ones:**
  ```bash
  cat ~/.claude/settings.json

  python3 -c "import json,os; f=os.path.expanduser('~/.claude/settings.json'); os.makedirs(os.path.dirname(f), exist_ok=True); d=json.load(open(f)) if os.path.exists(f) and os.path.getsize(f)>0 else {}; d['autoUpdatesChannel']='stable'; json.dump(d, open(f,'w'), indent=2)"
  ```

**Install the VS Code extension**
- Open VS Code
- Go to the Extensions view (click the square icon on the left sidebar or press `Cmd + Shift + X`)
- Search for "Claude Code" and click Install on the extension by Anthropic

**Clone the tutorial repo**
- Open Terminal
- Run:
  ```bash
  mkdir -p ~/projects
  cd ~/projects
  git clone https://github.com/anthropics/claude-code-best-practice.git
  git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
  cd YOUR-REPO
  code .
  ```
Now head back to [README.md](README.md) for authentication setup.
