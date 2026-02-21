import shutil
from pathlib import Path

import yaml


def get_man_binary() -> str:
    """Resolve the man binary path across different Linux distributions."""
    candidates = ["man"]
    for candidate in candidates:
        path = shutil.which(candidate)
        if path:
            return path
    raise FileNotFoundError(
        "Could not find 'man' binary. Please install man-db or man-pages."
    )


def get_themes_dir() -> Path:
    """Return the path to the bundled themes directory."""
    return Path(__file__).parent.parent / "themes"


def load_theme(name: str) -> dict:
    """Load a theme YAML file by name. Falls back to default if not found."""
    themes_dir = get_themes_dir()
    theme_file = themes_dir / f"{name}.yaml"

    if not theme_file.exists():
        theme_file = themes_dir / "default.yaml"

    with theme_file.open() as f:
        return yaml.safe_load(f)
