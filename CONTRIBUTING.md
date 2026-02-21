# Contributing to SmartMan

First off, thank you for considering contributing to SmartMan! It's people like you that make it a great tool.

## How Can I Contribute?

### 🎨 Adding New Themes
We love beautiful terminal aesthetics. To add a new theme:
1.  Create a new YAML file in `smartman/themes/`.
2.  Follow the structure of `default.yaml` or `dracula.yaml`.
3.  Test it using `smartman --theme <your_theme> ls`.
4.  Submit a PR!

### 🐛 Reporting Bugs
If you find a bug (especially with man page parsing), please open an issue and include:
*   The command you were running.
*   Your OS/Distribution.
*   The error message or a screenshot of the broken TUI.

### ✨ Feature Requests
Have an "out-of-the-box" idea? Open an issue and let's discuss it!

---

## Technical Setup
1.  **Clone**: `git clone https://github.com/your-username/smartman.git`
2.  **Dev Install**: `pip install -e .`
3.  **Run**: `smartman ls`

Happy coding! 🚀
