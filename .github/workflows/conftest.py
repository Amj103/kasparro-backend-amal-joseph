import pytest
from api.db import engine
from api.models import Base

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Force create all tables before any tests run
    Base.metadata.create_all(bind=engine)
    yield