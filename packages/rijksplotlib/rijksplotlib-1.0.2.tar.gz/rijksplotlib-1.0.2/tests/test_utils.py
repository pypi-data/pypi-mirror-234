"""Test the utils module."""
import os
from pathlib import Path
import rijksplotlib.utils as utils


def test_resolve_path():
    """Test the resolve_path function."""
    cwd = os.getcwd()
    assert utils.resolve_path("examples") == Path(os.path.join(cwd, "examples"))
