from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field

from smartman.utils import get_man_binary


SECTION_HEADERS = re.compile(
    r"^([A-Z][A-Z\s\-]+[A-Z])$", re.MULTILINE
)

KNOWN_SECTIONS = [
    "NAME",
    "SYNOPSIS",
    "DESCRIPTION",
    "OPTIONS",
    "EXAMPLES",
    "EXAMPLE",
    "EXIT STATUS",
    "RETURN VALUE",
    "ENVIRONMENT",
    "FILES",
    "SEE ALSO",
    "BUGS",
    "NOTES",
    "AUTHORS",
    "COPYRIGHT",
]


class ManPageNotFoundError(Exception):
    """Raised when a man page cannot be found for the given command."""

    def __init__(self, command: str) -> None:
        self.command = command
        super().__init__(f"No manual entry for '{command}'")


@dataclass
class ManPage:
    command: str
    raw_text: str
    sections: dict[str, str] = field(default_factory=dict)

    def get_section(self, name: str) -> str:
        """Return content of a section, case-insensitively."""
        for key, value in self.sections.items():
            if key.upper() == name.upper():
                return value
        return ""

    def get_quick_examples(self) -> list[dict[str, str]]:
        """Extract command + description pairs from the EXAMPLES section."""
        examples_text = self.get_section("EXAMPLES") or self.get_section("EXAMPLE")
        if not examples_text:
            return []

        examples = []
        # Basic heuristic: look for indented blocks (commands) and surrounding text
        # Many man pages use a pattern: Description\n    command
        lines = examples_text.splitlines()
        current_desc = ""
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            
            # If line is indented, it's likely a command
            if line.startswith("       ") or line.startswith("\t"):
                if current_desc:
                    examples.append({"desc": current_desc, "cmd": stripped})
                    current_desc = ""
                elif i > 0:
                    # Fallback: check previous line if it wasn't empty
                    prev = lines[i-1].strip()
                    if prev:
                        examples.append({"desc": prev, "cmd": stripped})
            else:
                current_desc = stripped

        # Limit to top 4 for the gallery
        return examples[:4]


class ManParser:
    """Parses Linux man page output into structured sections."""

    def parse(self, command: str) -> ManPage:
        raw = self._fetch_raw(command)
        sections = self._split_sections(raw)
        return ManPage(command=command, raw_text=raw, sections=sections)

    def _fetch_raw(self, command: str) -> str:
        man_bin = get_man_binary()
        parts = command.split()

        try:
            man_result = subprocess.run(
                [man_bin] + parts,
                capture_output=True,
                text=True,
                timeout=15,
                env={"MANPAGER": "cat", "PAGER": "cat", "PATH": "/usr/bin:/bin:/usr/local/bin"},
            )
        except FileNotFoundError as exc:
            raise ManPageNotFoundError(command) from exc
        except subprocess.TimeoutExpired as exc:
            raise ManPageNotFoundError(command) from exc

        if man_result.returncode != 0 or not man_result.stdout.strip():
            raise ManPageNotFoundError(command)

        raw = man_result.stdout

        col_result = subprocess.run(
            ["col", "-b"],
            input=raw,
            capture_output=True,
            text=True,
        )

        return col_result.stdout if col_result.returncode == 0 else raw

    def _split_sections(self, raw: str) -> dict[str, str]:
        sections: dict[str, str] = {}
        lines = raw.splitlines()
        current_section: str | None = None
        buffer: list[str] = []

        for line in lines:
            stripped = line.rstrip()
            if self._is_section_header(stripped):
                if current_section is not None:
                    sections[current_section] = "\n".join(buffer).strip()
                current_section = stripped.strip()
                buffer = []
            else:
                if current_section is not None:
                    buffer.append(stripped)

        if current_section is not None and buffer:
            sections[current_section] = "\n".join(buffer).strip()

        return sections

    def _is_section_header(self, line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if not line.startswith(" ") and stripped == stripped.upper():
            if len(stripped) >= 2 and stripped.replace(" ", "").replace("-", "").isalpha():
                return True
        return False

