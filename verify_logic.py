import sys
import os

# Add the current directory to sys.path to import from smartman package
sys.path.append(os.getcwd())

from smartman.parser.man_parser import ManParser
from smartman.renderer.formatter import Formatter
from smartman.utils import load_theme

def test_man_logic():
    print("--- 1. Testing Parser ---")
    parser = ManParser()
    try:
        page = parser.parse("ls")
        print(f"Command: {page.command}")
        print(f"Sections found: {list(page.sections.keys())}")
        
        # Check specific sections
        if "NAME" in page.sections:
            print(f"NAME section: {page.sections['NAME']}")
        if "SYNOPSIS" in page.sections:
            print(f"SYNOPSIS section: {page.sections['SYNOPSIS']}")
            
        print("\n--- 2. Testing Formatter (Markup Generation) ---")
        theme = load_theme("default")
        formatter = Formatter(theme)
        
        # Check if formatter generates what TUI needs
        markup = formatter.format_section_as_markup("NAME", page.sections.get("NAME", ""))
        print("Generated Markup for NAME:")
        print(markup)
        
        print("\n--- 3. Testing TUI Layout (Structure Check) ---")
        from smartman.renderer.tui import SmartManApp
        # We can't run the app, but we can check the class
        app = SmartManApp(page, theme)
        print(f"App title: {app.TITLE}")
        print(f"App bindings: {[b.key for b in app.BINDINGS]}")
        
        print("\nVerification Complete!")
        
    except Exception as e:
        import traceback
        print(f"Error during verification: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_man_logic()
