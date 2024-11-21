from __future__ import annotations

from pathlib import Path

import pytest
from streamdeck_cli.commands.pack.autoversion import get_versioned_output_dirpath


@pytest.fixture
def fake_output_dirpath(tmp_path: Path) -> Path:
    return tmp_path / "releases"


@pytest.fixture(params=[("1.0.0", None), ("1.3.0", 1), ("5.0.5", 3), ("0.0.1", 10)])
def plugin_version_and_previous_subversion(request: pytest.FixtureRequest, fake_output_dirpath: Path) -> tuple[str, int | None]:
    """Fixture to create a fake output directory with previous releases for a specified plugin version and subversions."""
    plugin_version, previous_subversion = request.param
    if previous_subversion is not None:
        # First create the original versioned release directory without a subversion,  ex: "1.0.0"
        previous_versioned_release_dirpath = fake_output_dirpath / f"{plugin_version}"
        previous_versioned_release_dirpath.mkdir(parents=True, exist_ok=True)

        # Then iterate over the subversions and create the versioned release directories with subversions, ex: "1.0.0-1", "1.0.0-2", etc.
        for subversion in range(1, previous_subversion + 1):
            previous_versioned_release_dirpath = fake_output_dirpath / f"{plugin_version}-{subversion}"
            previous_versioned_release_dirpath.mkdir(parents=True, exist_ok=True)

    return plugin_version, previous_subversion


def test_correct_output_version_and_subversion(fake_output_dirpath: Path, plugin_version_and_previous_subversion: tuple[str, int | None]):
    """Test that the correct versioned output directory path is returned for a plugin version with previous releases.

    NOTE: This test is parameterized to test multiple plugin versions with and without previous subversions.
    """
    plugin_version, previous_subversion = plugin_version_and_previous_subversion

    # Determine the expected output directory path based on the plugin version and previous subversion
    next_subversion: str = f"-{previous_subversion + 1}" if previous_subversion is not None else ""
    expected_path = fake_output_dirpath / f"{plugin_version}{next_subversion}"

    actual_path = get_versioned_output_dirpath(fake_output_dirpath, plugin_version)

    assert actual_path == expected_path
