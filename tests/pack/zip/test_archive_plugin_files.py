"""Tests for the archive_plugin_files function in the pack module."""
import zipfile
from pathlib import Path

import pathspec
import pytest
from pathspec.patterns.gitwildmatch import GitWildMatchPattern
from streamdeck_cli.commands.pack import archive_plugin_files


@pytest.fixture
def plugin_dirpath(tmp_path: Path) -> Path:
    """Fixture to define the plugin directory path for the plugin to be packed from."""
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    (plugin_dir / "file1.txt").write_text("content1")
    (plugin_dir / "file2.txt").write_text("content2")

    # Create a .packignore file in the plugin_dirpath, which should be ignored by the code
    (plugin_dir / ".packignore").write_text(".packignore")

    return plugin_dir


@pytest.fixture
def output_filepath(tmp_path: Path) -> Path:
    """Fixture to define the output file path for the plugin to be packed into."""
    return tmp_path / "output.streamDeckPlugin"


@pytest.fixture
def packignore_spec() -> pathspec.PathSpec:
    """Fixture to create a PathSpec object that matches 'file2.txt' and '.packignore'."""
    # Create a PathSpec object that would be created from the .packignore file to ignore 'file2.txt' and '.packignore'
    ignore_patterns = [".packignore"]
    return pathspec.PathSpec.from_lines(GitWildMatchPattern, ignore_patterns)


def test_archive_plugin_files(plugin_dirpath: Path, output_filepath: Path, packignore_spec: pathspec.PathSpec):
    """Test that the archive_plugin_files function archives the plugin files into a new zip file."""
    # Create a .packignore file in the plugin_dirpath
    plugin_uuid = "test_plugin"
    archive_plugin_files(plugin_dirpath, output_filepath, plugin_uuid=plugin_uuid, packignore_spec=packignore_spec)

    with zipfile.ZipFile(output_filepath, "r") as zip_file:
        unique_filepaths = set(zip_file.namelist())
        # The files should be stored in the zip file under a base directory with the name of the plugin UUID found in the manifest, appended with ".sdPlugin"
        assert unique_filepaths == {f"{plugin_uuid}.sdPlugin/file1.txt", f"{plugin_uuid}.sdPlugin/file2.txt"}
