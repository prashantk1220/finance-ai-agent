import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.postgres_client import Base, get_db


@pytest.fixture(scope="function")
def test_session():
    """Fixture to create a mock database session for testing."""
    # Use SQLite in-memory database for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# Override get_db to use test_session
@pytest.fixture(scope="function")
def override_get_db(test_session):
    """Override the get_db dependency to use the test session in App"""
    def _get_db():
        yield test_session
    app.dependency_overrides[get_db] = _get_db
    return test_session