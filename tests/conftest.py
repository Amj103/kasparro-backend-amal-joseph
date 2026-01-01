import pytest
from api.db import engine
from api.models import Base

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    This runs once at the very start of the test session.
    It forces SQLAlchemy to create all tables in the database.
    """
    Base.metadata.create_all(bind=engine)
    yield