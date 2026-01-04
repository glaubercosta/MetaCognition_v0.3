import pytest
from app.db import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Initialize the database before running tests.
    This fixture runs once per test session and ensures tables are created.
    """
    init_db()
