from __future__ import annotations

import re

from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text

from smartman.parser.man_parser import ManPage


FLAG_PATTERN = re.compile(r"(-{1,2}[a-zA-Z][\w-]*)")
SYNOPSIS_CODE_PATTERN = re.compile(r"(`[^`]+`|\[[^\]]+\]|<[^>]+>)")


class Formatter:
    """Rich-based formatter for man page sections."""

    def __init__(self, theme: dict) -> None:
        self.theme = theme
        self.console = Console()

    def render_plain(self, page: ManPage) -> None:
        """Render the full man page to stdout using Rich markup."""
        self._print_header(page.command)

        for section_name, content in page.sections.items():
            self._print_section(section_name, content)

    def _print_header(self, command: str) -> None:
        heading_style = self.theme.get("heading", "bold cyan")
        accent = self.theme.get("accent", "cyan")

        self.console.print()
        self.console.print(
            Panel(
                Text(f" {command.upper()} ", style=f"bold {heading_style}", justify="center"),
                style=accent,
                subtitle=f"[{self.theme.get('muted', 'dim white')}]smartman — modern man page viewer[/]",
                expand=True,
            )
        )
        self.console.print()

    def _print_section(self, name: str, content: str) -> None:
        heading_style = self.theme.get("heading", "bold cyan")
        border_style = self.theme.get("border", "blue")

        self.console.print(Rule(f"[{heading_style}]{name}[/]", style=border_style))

        if name.upper() == "SYNOPSIS":
            self._render_synopsis(content)
        elif name.upper() == "OPTIONS":
            self._render_options(content)
        else:
            self._render_body(content)

        self.console.print()

    def _render_synopsis(self, content: str) -> None:
        synopsis_style = self.theme.get("synopsis", "italic bright_green")
        flag_style = self.theme.get("flag", "bold yellow")
        styled = Text()
        for line in content.splitlines():
            parts = FLAG_PATTERN.split(line)
            for i, part in enumerate(parts):
                if FLAG_PATTERN.match(part):
                    styled.append(part, style=flag_style)
                else:
                    styled.append(part, style=synopsis_style)
            styled.append("\n")
        self.console.print(Padding(styled, (0, 4)))

    def _render_options(self, content: str) -> None:
        flag_style = self.theme.get("flag", "bold yellow")
        desc_style = self.theme.get("description", "white")

        for line in content.splitlines():
            text = Text()
            parts = FLAG_PATTERN.split(line)
            for part in parts:
                if FLAG_PATTERN.match(part):
                    text.append(part, style=flag_style)
                else:
                    text.append(part, style=desc_style)
            self.console.print(Padding(text, (0, 4)))

    def _render_body(self, content: str) -> None:
        desc_style = self.theme.get("description", "white")
        flag_style = self.theme.get("flag", "bold yellow")
        highlight_style = self.theme.get("highlight", "bold magenta")

        for line in content.splitlines():
            text = Text()
            parts = FLAG_PATTERN.split(line)
            for part in parts:
                if FLAG_PATTERN.match(part):
                    text.append(part, style=flag_style)
                else:
                    text.append(part, style=desc_style)
            self.console.print(Padding(text, (0, 2)))

    def format_section_as_markup(self, name: str, content: str) -> str:
        """Return a section formatted as Rich markup string (used by TUI)."""
        lines = [f"[bold cyan]{name}[/]", ""]
        flag_open = f"[{self.theme.get('flag', 'bold yellow')}]"
        flag_close = "[/]"
        desc = self.theme.get("description", "white")

        for line in content.splitlines():
            parts = FLAG_PATTERN.split(line)
            out = ""
            for part in parts:
                if FLAG_PATTERN.match(part):
                    out += f"[bold yellow]{part}[/bold yellow]"
                else:
                    escaped = part.replace("[", r"\[")
                    out += f"[{desc}]{escaped}[/{desc}]"
            lines.append(out)

        return "\n".join(lines)
