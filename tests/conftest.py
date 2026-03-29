import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.database import init_db
import pytest

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.fixture
def simple_text():
    return "The boy kicked the ball. He ran after it. The girl saw him."

@pytest.fixture
def long_text():
    return """
    Last summer, Emma decided to try something new.
    She joined a volunteer program in a small village near the mountains.
    Emma and other volunteers worked together to repair an old community center.
    Every morning they painted walls and fixed broken windows.
    The villagers were very kind and grateful for their help.
    """