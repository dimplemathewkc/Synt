import pytest
from starlette.testclient import TestClient
from backend.app.main import get_application


@pytest.fixture
def client():
    app = get_application()
    with TestClient(app) as client:
        yield client
