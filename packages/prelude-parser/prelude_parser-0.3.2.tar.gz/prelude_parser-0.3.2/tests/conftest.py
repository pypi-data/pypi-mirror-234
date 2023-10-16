from pathlib import Path

import pytest

ASSETS_PATH = Path().absolute() / "tests/assets"


@pytest.fixture
def test_file_1():
    return ASSETS_PATH / "test1.xml"


@pytest.fixture
def test_file_2():
    return ASSETS_PATH / "test2.xml"


@pytest.fixture
def test_file_3():
    return ASSETS_PATH / "test3.xml"


@pytest.fixture
def test_file_4():
    return ASSETS_PATH / "test4.xml"
