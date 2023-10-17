#!/usr/bin/env python3

import os
import tempfile

import pytest

@pytest.fixture(autouse=True)
def no_config_file(monkeypatch):
	path = tempfile.mkdtemp()
	monkeypatch.setitem(os.environ, 'XDG_CONFIG_HOME', path)
	yield
	os.rmdir(path)
