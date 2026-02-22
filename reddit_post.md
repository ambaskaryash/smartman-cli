# POST TITLE:
I got tired of squinting at man pages so I built a TUI replacement for `man` [OC]

---

# POST BODY:
(for r/commandline, r/linux, r/Python)

---

`man grep` works. It's just not *pleasant*.

So I spent the last few weeks building **SmartMan CLI** — a drop-in replacement 
for the `man` command with a proper TUI, syntax highlighting, a sidebar for 
jumping between sections, and AI-powered plain-English explanations for when 
the formal spec language isn't helping.

**Demo:** https://vhs.charm.sh/vhs-3vIvVmHvhKGBzRqjQ3UPyf.gif

**Install in one line:**
```
curl -sSL https://raw.githubusercontent.com/ambaskaryash/smartman-cli/main/install.sh | bash
```

Then alias it:
```
alias man='smartman'
```

Built with Python, Textual, and Rich. Themes included (Dracula, Catppuccin, Nord, Monokai).

Source: https://github.com/ambaskaryash/smartman-cli

---

**What's the one thing you wish man pages did better?** 
Genuinely asking — building a roadmap and want real pain points.

---