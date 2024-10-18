from pathlib import Path

from gilbert.plugins.yaml import load_yaml


def test_yaml_plugin():
    """Test the content being read from a YAML header, followed by Markdown

    This is a regression test for a fix for an off-by-one issue where the 8192nd
    character in the YAML/Markdown document could be missing from the rendered
    Markdown due to the way the YAML loader buffer was being sliced.
    """
    path = Path(__file__).resolve().parent / "plugin_data" / "test_content.yaml"

    data, meta = load_yaml(path)

    assert meta == {
        "title": "Test more than 8192 characters",
        "content_type": "MarkdownPage",
    }

    # Ensure that "READ" doesn't become "REA":
    assert "PLEASE READ THIS LINE CAREFULLY" in data
