"""Tests that the get_packignore_specification function either returns a pathspec.PathSpec object if the .packignore file exists, or raises a typer.Exit exception if the file is missing."""
from __future__ import annotations

from pathlib import Path

import pytest
import typer
from streamdeck_cli.commands.pack.zip import get_packignore_specification


@pytest.fixture
def plugin_dirpath_with_packignore(tmp_path: Path) -> Path:
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    (plugin_dir / ".packignore").write_text("file2.txt")
    return plugin_dir


@pytest.fixture
def plugin_dirpath_without_packignore(tmp_path: Path) -> Path:
    plugin_dir = tmp_path / "plugin"
    plugin_dir.mkdir()
    return plugin_dir


def test_get_packignore_specification_with_packignore(plugin_dirpath_with_packignore: Path):
    spec = get_packignore_specification(plugin_dirpath_with_packignore)
    assert spec.match_file("file2.txt")
    assert not spec.match_file("file1.txt")


def test_get_packignore_specification_without_packignore(plugin_dirpath_without_packignore: Path):
    with pytest.raises(typer.Exit) as exc_info:
        get_packignore_specification(plugin_dirpath_without_packignore)
    assert exc_info.value.exit_code == 9
