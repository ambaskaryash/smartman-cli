# 📖 SmartMan CLI

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Built with Textual](https://img.shields.io/badge/built%20with-Textual-hotpink.svg)](https://textual.textualize.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![SmartMan CLI Demo](https://vhs.charm.sh/vhs-3vIvVmHvhKGBzRqjQ3UPyf.gif)

**SmartMan CLI** is a modern, terminal-native enhancement for the Linux `man` command. It transforms dense, hard-to-read manual pages into an interactive, visually stunning experience with syntax highlighting, quick-navigation sidebars, and AI-powered explanations.

```text
 ____                        _   __  __
/ ___| _ __ ___   __ _ _ __ | |_|  \/  | __ _  _ __
\___ \| '_ ` _ \ / _` | '__|| __| |\/| |/ _` | '_ \
 ___) | | | | | | (_| | |   | |_| |  | | (_| | | | |
|____/|_| |_| |_|\__,_|_|    \__|_|  |_|\__,_|_| |_|
```

---

## ✨ Features

*   **⚡ Modern TUI**: A beautiful, responsive terminal interface built with Textual.
*   **🚀 Quick-Win Gallery**: Interactive "cards" at the top of every page showing the most common usage examples.
*   **📂 Interactive Sidebar**: Instantly jump between NAME, SYNOPSIS, DESCRIPTION, and OPTIONS.
*   **🎨 Syntax Highlighting**: Automatic coloring for flags, parameters, and code snippets.
*   **🤖 AI-Powered Explanations**: Stressed by a complex flag? Use `--explain` for a plain-English breakdown.
*   **🌈 Theming Support**: Choose between `default`, `dracula`, and `monokai` out of the box.

---

## 🚀 Installation

### The One-Liner (Recommended)
Install SmartMan CLI globally with a single command:
```bash
curl -sSL https://raw.githubusercontent.com/ambaskaryash/smartman-cli/main/install.sh | bash
```

### Global (via pipx)
```bash
pipx install .
```

### macOS/Linux (via Homebrew)
```bash
# After you've hosted your formula
brew install ambaskaryash/tap/smartman
```

---

## 🤖 AI Explanations (Powered by Groq)

SmartMan CLI uses the lightning-fast **Groq API** to provide instant, plain-English explanations of complex manual pages.

1.  Get a free API key from [Groq Console](https://console.groq.com/).
2.  Export it in your shell:
    ```bash
    export GROQ_API_KEY='your_key_here'
    ```
3.  Run:
    ```bash
    smartman --explain grep
    ```

## 🛠 Usage

Simply prefix any command you would normally use with `man` with `smartman`:

```bash
smartman grep
```

### Commands & Flags
*   `smartman <command>`: Launch the full interactive TUI.
*   `smartman --plain <command>`: Fall back to a beautiful Rich-rendered plain text view (great for quick lookups).
*   `smartman --theme dracula <command>`: Use a different theme.
*   `smartman --explain <command>`: Get an AI-powered summary of what the command does.

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `n` | Jump to **NAME** |
| `s` | Jump to **SYNOPSIS** |
| `d` | Jump to **DESCRIPTION** |
| `o` | Jump to **OPTIONS** |
| `e` | Jump to **EXAMPLES** |
| `q` | Quit |

---

## 🐚 Shell Integration (Highly Recommended)

Make SmartMan your default manual viewer by adding an alias to your shell configuration (`.bashrc` or `.zshrc`):

```bash
alias man='smartman'
```

Now, whenever you type `man <command>`, you'll get the full SmartMan experience!

---

## 🎨 Themes

SmartMan supports custom YAML themes. You can find the bundled themes in `smartman/themes/`.

| Theme | Preview |
|-------|---------|
| **Default** | *Modern Dark Blue* |
| **Dracula** | *Classic Dev aesthetic* |
| **Monokai** | *High-contrast vibrant* |
| **Nord**    | *Cool-toned Frost* |
| **Catppuccin** | *Pastel Mocha* |

---

## 🤝 Contributing

We love stars! ⭐ If you find this tool useful, please give it a star and share it with your fellow Linux users.

1.  Fork the repo.
2.  Create your feature branch.
3.  Add a new theme in `smartman/themes/`.
4.  Submit a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

*Built with ❤️ by [ambaskaryash](https://github.com/ambaskaryash)*
