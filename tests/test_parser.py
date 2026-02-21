import pytest
from smartman.parser.man_parser import ManParser

def test_parser_basic():
    """Test that the parser can fetch and parse a basic command."""
    parser = ManParser()
    page = parser.parse("ls")
    
    assert page.command == "ls"
    assert "NAME" in page.sections
    assert "SYNOPSIS" in page.sections
    assert len(page.raw_text) > 0

def test_get_section():
    """Test case-insensitive section retrieval."""
    parser = ManParser()
    page = parser.parse("grep")
    
    # Try different cases
    content = page.get_section("description")
    assert content != ""
    assert page.get_section("DESCRIPTION") == content
    assert page.get_section("NoExist") == ""

def test_get_quick_examples():
    """Test that examples are extracted correctly."""
    parser = ManParser()
    page = parser.parse("grep")
    
    examples = page.get_quick_examples()
    # Most Linux systems have examples for grep
    assert isinstance(examples, list)
    if examples:
        assert "cmd" in examples[0]
        assert "desc" in examples[0]
