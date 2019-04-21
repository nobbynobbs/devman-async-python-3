"""pytest configuration file. define common fixtures etc."""

import os

import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def file_path():
    return os.path.join(TESTS_DIR, "test-files", "random-bytes")


@pytest.fixture
def file_content(file_path):
    with open(file_path, "rb") as f_h:
        return f_h.read()
