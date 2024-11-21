from pathlib import Path

import pathspec
import pytest
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
from streamdeck_cli.commands.pack.zip import walk_filtered_plugin_files


@pytest.fixture
def plugin_dirpath(tmp_path: Path) -> Path:
    """Fixture to create a plugin directory with a .packignore file and two files to test on."""
    # Create a plugin directory
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()

    # Create two files in the plugin directory — one of which should be ignored by the code
    (plugin_dir / "file1.txt").write_text("content1")
    (plugin_dir / "file2.txt").write_text("content2")

    # The .packignore file should be ignored by the code
    (plugin_dir / ".packignore").write_text("file2.txt\n.packignore")

    return plugin_dir


@pytest.fixture
def packignore_spec() -> pathspec.PathSpec:
    """Fixture to create a PathSpec object that matches 'file2.txt' and '.packignore'."""
    # Create a PathSpec object that would be created from the .packignore file to ignore 'file2.txt' and '.packignore'
    ignore_patterns = ["file2.txt", ".packignore"]
    return pathspec.PathSpec.from_lines(GitWildMatchPattern, ignore_patterns)


def test_walk_filtered_plugin_files(plugin_dirpath: Path, packignore_spec: pathspec.PathSpec):
    """Test that the walk_filtered_plugin_files function yields files that are not ignored."""
    files = list(walk_filtered_plugin_files(plugin_dirpath, packignore_spec))
    assert files == [Path("file1.txt")]
