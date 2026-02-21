import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from smartman import __version__
from smartman.parser.man_parser import ManParser, ManPageNotFoundError
from smartman.renderer.formatter import Formatter
from smartman.renderer.tui import SmartManApp
from smartman.utils import load_theme
from smartman.utils.ai import explain_command
from smartman.utils.tips import get_random_tip

app = typer.Typer(
    name="smartman",
    help="SmartMan — Modern Linux Man Page Enhancer CLI",
    add_completion=False,
)
console = Console()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    command: Optional[list[str]] = typer.Argument(None, help="The command to look up"),
    version: Optional[bool] = typer.Option(None, "--version", "-v", help="Show version", is_eager=True),
    plain: bool = typer.Option(False, "--plain", help="Force plain output mode"),
    theme_name: str = typer.Option("default", "--theme", "-t", help="Visual theme to use"),
    explain: bool = typer.Option(False, "--explain", help="Get AI-powered explanation"),
    tip: bool = typer.Option(False, "--tip", help="Show a random Linux tip"),
):
    """
    Enhanced man page viewer with structured sections and TUI.
    """
    if version:
        console.print(f"SmartMan version: [bold cyan]{__version__}[/bold cyan]")
        raise typer.Exit()

    if tip:
        t = get_random_tip()
        console.print()
        console.print(Panel(
            t["content"],
            title=f"[bold yellow]💡 SmartMan Tip: {t['title']}[/bold yellow]",
            subtitle="[dim]Run 'smartman --tip' for more![/dim]",
            border_style="yellow",
            padding=(1, 2)
        ))
        console.print()
        raise typer.Exit()

    if not command:
        console.print("[bold yellow]Usage:[/bold yellow] smartman <command>")
        console.print("Try [bold cyan]smartman --help[/bold cyan] for more info.")
        raise typer.Exit()

    # Join multi-word commands (smartman docker run)
    cmd_str = " ".join(command)

    if explain:
        try:
            parser = ManParser()
            with console.status(f"[bold blue]Fetching manual for {cmd_str} for AI explanation...[/bold blue]"):
                page = parser.parse(cmd_str)
        except ManPageNotFoundError as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred during man page fetch for AI:[/bold red] {e}")
            sys.exit(1)

        with console.status(f"[bold blue]Generating AI explanation for {cmd_str}...[/bold blue]"):
            explanation_text = explain_command(cmd_str, page.raw_text)

        console.print(Panel(
            explanation_text,
            title=f"[bold green]AI Explanation for {cmd_str.upper()}[/bold green]",
            border_style="green",
            expand=False
        ))
        raise typer.Exit()

    try:
        # Load theme
        try:
            theme_dict = load_theme(theme_name)
        except Exception:
            theme_dict = load_theme("default")

        # Parse man page
        parser = ManParser()
        with console.status(f"[bold blue]Fetching manual for {cmd_str}...[/bold blue]"):
            page = parser.parse(cmd_str)

        if plain:
            # Rich plain rendering
            formatter = Formatter(theme_dict)
            formatter.render_plain(page)
        else:
            # Textual TUI
            tui_app = SmartManApp(page, theme_dict)
            tui_app.run()

    except ManPageNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    app()
