from __future__ import annotations

import re
from rich.console import Group
from rich.rule import Rule
from rich.text import Text
from rich.panel import Panel

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.css.query import NoMatches
from textual.widgets import Footer, Header, Label, ListItem, ListView, Static, Input
from textual.reactive import reactive

from smartman.parser.man_parser import ManPage
from smartman.renderer.formatter import Formatter


class QuickExampleCard(Static):
    """A single example card for the Quick-Win Gallery."""
    
    DEFAULT_CSS = """
    QuickExampleCard {
        width: 35;
        height: 8;
        background: $accent 10%;
        border: solid $accent;
        padding: 1 2;
        margin: 0 1;
    }
    .example-cmd {
        color: $accent;
        text-style: bold;
        background: $background;
        padding: 0 1;
    }
    .example-desc {
        color: $text-muted;
        text-style: italic;
    }
    """

    def __init__(self, desc: str, cmd: str) -> None:
        super().__init__()
        self.desc = desc
        self.cmd = cmd

    def render(self) -> str:
        return f"[i dim]{self.desc}[/]\n\n[b cyan]> {self.cmd}[/]"


class SmartManApp(App):
    """Textual TUI application for SmartMan."""

    TITLE = "SmartMan"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("j", "scroll_down", "Scroll Down", show=False),
        Binding("k", "scroll_up", "Scroll Up", show=False),
        Binding("gg", "scroll_top", "Top", show=False),
        Binding("G", "scroll_bottom", "Bottom", show=False),
        Binding("n", "jump_section('NAME')", "NAME", show=True),
        Binding("s", "jump_section('SYNOPSIS')", "SYNOPSIS", show=True),
        Binding("d", "jump_section('DESCRIPTION')", "DESCRIPTION", show=True),
        Binding("o", "jump_section('OPTIONS')", "OPTIONS", show=True),
        Binding("e", "jump_section('EXAMPLES')", "EXAMPLES", show=True),
        Binding("/", "toggle_search", "Search", show=True),
        Binding("escape", "hide_search", "Close Search", show=False),
        Binding("?", "toggle_help", "Help", show=False),
    ]

    CSS = """
    Screen {
        background: #0d1117;
    }

    Header {
        background: $accent;
        color: auto;
        text-style: bold;
    }

    Footer {
        background: $surface;
        color: $text-muted;
    }

    #layout {
        layout: horizontal;
        height: 1fr;
    }

    #sidebar {
        width: 22;
        border-right: solid $accent;
        background: $surface;
    }

    #sidebar-title {
        width: 22;
        text-align: center;
        background: $accent 30%;
        color: $accent;
        text-style: bold;
        padding: 1 1;
        border-bottom: solid $accent;
    }

    #section-list {
        background: transparent;
        border: none;
    }

    .section-label {
        padding: 0 1;
        color: $text-muted;
    }

    .section-label:hover {
        color: $accent;
        background: $accent 10%;
    }

    #content-area {
        height: 1fr;
    }

    #main-scroll {
        height: 1fr;
        padding: 1 3;
    }

    #gallery {
        height: auto;
        margin: 1 0;
        padding: 1 0;
        border-bottom: double $accent;
        display: none;
    }

    #gallery.has-examples {
        display: block;
    }

    #gallery-label {
        color: $accent;
        text-style: bold italic;
        margin-left: 2;
        margin-bottom: 1;
    }

    .gallery-container {
        layout: horizontal;
        height: auto;
        overflow-x: auto;
    }

    .man-section {
        margin-bottom: 2;
    }

    .section-content {
        padding-left: 4;
        color: $text;
    }

    #search-bar {
        display: none;
        height: 3;
        background: $surface;
        border: tall $accent;
        padding: 0 1;
        margin: 0 1;
        dock: bottom;
    }

    #search-bar.visible {
        display: block;
    }

    #search-input {
        width: 1fr;
        border: none;
        background: transparent;
    }
    """

    show_search = reactive(False)

    def __init__(self, page: ManPage, theme: dict) -> None:
        super().__init__()
        self.page = page
        self.theme_data = theme
        self.formatter = Formatter(theme)
        self._section_widgets: dict[str, Static] = {}
        self._last_search = ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="layout"):
            with Container(id="sidebar"):
                yield Static(f" 📖 {self.page.command.upper()}", id="sidebar-title")
                sidebar = ListView(id="section-list")
                yield sidebar

            with Vertical(id="content-area"):
                with Container(id="gallery"):
                    yield Label("✨ QUICK-WIN EXAMPLES", id="gallery-label")
                    with Horizontal(classes="gallery-container", id="gallery-cards"):
                        pass
                
                with VerticalScroll(id="main-scroll"):
                    pass
                
                with Horizontal(id="search-bar"):
                    yield Label("🔍 ", id="search-icon")
                    yield Input(placeholder="Search keywords...", id="search-input")

        yield Footer()

    def on_mount(self) -> None:
        self.title = f"SmartMan — {self.page.command}"
        self.sub_title = "Press / to search | q to quit"

        sidebar = self.query_one("#section-list", ListView)
        content_container = self.query_one("#main-scroll", VerticalScroll)

        # 1. Populating Gallery
        examples = self.page.get_quick_examples()
        if examples:
            gallery = self.query_one("#gallery")
            gallery.add_class("has-examples")
            cards_container = self.query_one("#gallery-cards")
            for ex in examples:
                cards_container.mount(QuickExampleCard(ex["desc"], ex["cmd"]))

        # 2. Populating Sections
        for section_name, content in self.page.sections.items():
            safe_name = section_name.replace(' ', '_')
            item = ListItem(
                Label(f" {section_name}", classes="section-label"),
                id=f"nav-{safe_name}",
            )
            sidebar.append(item)

            section_widget = self._create_section_widget(section_name, content)
            self._section_widgets[section_name.upper()] = section_widget
            content_container.mount(section_widget)

    def _create_section_widget(self, name: str, content: str, highlight_query: str = "") -> Static:
        """Create a styled Static widget for a man page section."""
        from rich.rule import Rule
        from rich.text import Text
        from rich.console import Group
        import re

        heading_style = self.theme_data.get("heading", "bold cyan")
        flag_style = self.theme_data.get("flag", "bold yellow")
        desc_style = self.theme_data.get("description", "white")
        synopsis_style = self.theme_data.get("synopsis", "italic bright_green")
        border_style = self.theme_data.get("border", "blue")
        search_style = "bold white on magenta"
        
        FLAG_PAT = re.compile(r"(-{1,2}[a-zA-Z][\w-]*)")

        renderables = []
        renderables.append(Rule(f"[{heading_style}]{name}[/]", style=border_style))
        renderables.append(Text("")) # Spacer

        for line in content.splitlines():
            text = Text()
            parts = FLAG_PAT.split(line)
            for part in parts:
                if FLAG_PAT.match(part):
                    style = flag_style
                elif name.upper() == "SYNOPSIS":
                    style = synopsis_style
                else:
                    style = desc_style
                
                # Apply search highlighting if query exists
                if highlight_query and highlight_query.lower() in part.lower():
                    # Simple split-and-style for search
                    search_parts = re.split(f"({re.escape(highlight_query)})", part, flags=re.IGNORECASE)
                    for s_part in search_parts:
                        if s_part.lower() == highlight_query.lower():
                            text.append(s_part, style=search_style)
                        else:
                            text.append(s_part, style=style)
                else:
                    text.append(part, style=style)
            renderables.append(text)

        return Static(Group(*renderables), classes="man-section", id=f"section-{name.replace(' ', '_')}")

    def watch_show_search(self, show: bool) -> None:
        """Toggle search bar visibility."""
        search_bar = self.query_one("#search-bar")
        if show:
            search_bar.add_class("visible")
            self.query_one("#search-input").focus()
        else:
            search_bar.remove_class("visible")
            # If we cleared search, re-render sections to remove highlights
            if self._last_search:
                self._last_search = ""
                self._refresh_content()

    def action_toggle_search(self) -> None:
        self.show_search = not self.show_search

    def action_hide_search(self) -> None:
        self.show_search = False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Perform search when user presses Enter."""
        query = event.value.strip()
        if not query:
            self.show_search = False
            return

        self._last_search = query
        self._refresh_content(query)
        self._jump_to_first_match(query)

    def _refresh_content(self, query: str = "") -> None:
        """Update all section widgets with search highlights."""
        content_container = self.query_one("#main-scroll", VerticalScroll)
        # Clear current section widgets from container
        for widget in self._section_widgets.values():
            widget.remove()
        
        self._section_widgets.clear()
        
        # Re-mount with highlight
        for section_name, content in self.page.sections.items():
            section_widget = self._create_section_widget(section_name, content, query)
            self._section_widgets[section_name.upper()] = section_widget
            content_container.mount(section_widget)

    def _jump_to_first_match(self, query: str) -> None:
        """Find the first section containing the query and scroll to it."""
        for name, content in self.page.sections.items():
            if query.lower() in content.lower() or query.lower() in name.lower():
                self.action_jump_section(name)
                break

    def action_jump_section(self, section: str) -> None:
        """Scroll content to a specific section."""
        section_upper = section.upper()
        if section_upper in self._section_widgets:
            widget = self._section_widgets[section_upper]
            content_container = self.query_one("#main-scroll", VerticalScroll)
            content_container.scroll_to_widget(widget, animate=True)
            
            target_id = f"nav-{section.replace(' ', '_')}"
            try:
                sidebar = self.query_one("#section-list", ListView)
                for i, item in enumerate(sidebar.query(ListItem)):
                    if item.id == target_id:
                        sidebar.index = i
                        break
            except NoMatches:
                pass

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item and event.item.id:
            section_name = event.item.id.replace("nav-", "").replace("_", " ").upper()
            if section_name in self._section_widgets:
                widget = self._section_widgets[section_name]
                self.query_one("#main-scroll", VerticalScroll).scroll_to_widget(widget, animate=True)

    def action_scroll_down(self) -> None:
        """Scroll down slightly."""
        self.query_one("#main-scroll", VerticalScroll).scroll_down(animate=False)

    def action_scroll_up(self) -> None:
        """Scroll up slightly."""
        self.query_one("#main-scroll", VerticalScroll).scroll_up(animate=False)

    def action_scroll_top(self) -> None:
        """Scroll to the very top."""
        self.query_one("#main-scroll", VerticalScroll).scroll_to(0, 0, animate=True)

    def action_scroll_bottom(self) -> None:
        """Scroll to the very bottom."""
        self.query_one("#main-scroll", VerticalScroll).scroll_to(0, 1000000, animate=True)

    def action_toggle_help(self) -> None:
        self.notify(
            "/=Search  n=NAME  s=SYNOPSIS  d=DESCRIPTION  o=OPTIONS  e=EXAMPLES  q=Quit",
            title="Keyboard Shortcuts",
            timeout=5,
        )
