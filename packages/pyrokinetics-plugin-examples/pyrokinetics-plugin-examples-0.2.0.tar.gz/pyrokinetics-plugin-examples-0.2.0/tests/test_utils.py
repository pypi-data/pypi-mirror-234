from pathlib import Path

import pytest

from pyrokinetics_plugin_examples.utils import make_plugin_example_file, verify


def test_verify(tmp_path: Path):
    d = tmp_path / "pyrokinetics_plugin_examples"
    d.mkdir(parents=True, exist_ok=True)
    filename = d / "hello.txt"

    # Create standard example file
    make_plugin_example_file(filename)

    # Ensure no exception is raised when reading it
    verify(filename)

    # Modify the file so that it contains something else
    filename.write_text("Foo\n")

    # Expect verify to raise
    with pytest.raises(Exception):
        verify(filename)
