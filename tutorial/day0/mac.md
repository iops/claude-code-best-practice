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

**Install obsidian**
- Go to https://obsidian.md/download
- Click "Download for macOS"
- Open the downloaded .dmg file and drag Obsidian to your Applications folder
- Open Obsidian and create a new vault (e.g., "Claude Notes") in your Documents folder


**Clone the karpathy skills CLAUDE.md**
- Open Terminal
- Run:
  # Set up Andrej Karpathy skills - CLAUDE.md for all projects

  ```bash
  cd ~/.claude
  mkdir ~/.claude/rules
  mkdir -p ~/projects

  echo "" >> CLAUDE.md
  curl https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md >> CLAUDE.md

  curl https://raw.githubusercontent.com/iops/product-mode/refs/heads/main/CLAUDE.md >> ~/projects/CLAUDE.md
  ```

  # Set up LLM wiki

  ```bash
  mkdir -p ~/wiki-root
  claude
  Help me set up a LLM wiki that fits my needs and workflows
  https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  ```
  
  # Clone the claude-best-practices repo

  ```bash
  mkdir -p ~/projects
  cd ~/projects
  git clone https://github.com/iops/claude-code-best-practice.git
  cd claude-code-best-practice
  ```
Now head back to [README.md](README.md) for authentication setup.
