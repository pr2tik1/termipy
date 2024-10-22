import pytest
import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_env():
    # Set up any environment variables or configurations needed for tests
    os.environ["TERMIPY_TEST_MODE"] = "1"
    yield
    # Clean up after tests
    os.environ.pop("TERMIPY_TEST_MODE", None)