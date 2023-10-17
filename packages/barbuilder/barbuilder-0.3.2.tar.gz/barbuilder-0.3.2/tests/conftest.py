import os
import pathlib
import subprocess

import pytest


os.environ['SWIFTBAR_PLUGIN_PATH'] = '/path/to/script.py'

@pytest.fixture
def script_path():
    return pathlib.Path(os.environ['SWIFTBAR_PLUGIN_PATH'])

@pytest.fixture
def mock_subprocess(monkeypatch):

    def mock_run(*args, **kwargs):
        return args, kwargs

    monkeypatch.setattr(subprocess, 'run', mock_run)
