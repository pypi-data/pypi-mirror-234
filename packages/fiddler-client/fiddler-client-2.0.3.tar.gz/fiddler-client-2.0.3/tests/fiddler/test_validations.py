import tempfile
from pathlib import Path

import pytest

from fiddler.utils.validations import validate_artifact_dir


def test_validate_artifact_dir() -> None:
    # No dir
    with pytest.raises(ValueError) as cx:
        validate_artifact_dir(Path('/foo/bar'))

    assert str(cx.value) == '/foo/bar is not a valid model directory'

    # No package.py file
    with tempfile.TemporaryDirectory() as tmp:
        with pytest.raises(ValueError) as cx:
            validate_artifact_dir(Path(tmp))

        assert str(cx.value) == f'package.py file not found at {tmp}/package.py'
