import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_sign_message():
    """
    Test sign message.
    """
    response = client.get(
        "/crypto/sign?message=hello&webhook=http://localhost:8000/crypto/verify"
    )
    assert response.status_code == 202


def test_sign_message_with_cache():
    """
    Test sign message with cache.
    """
    response = client.get(
        "/crypto/sign?message=hello&webhook=http://localhost:8000/crypto/verify"
    )
    assert response.status_code == 202

    response = client.get(
        "/crypto/sign?message=hello&webhook=http://localhost:8000/crypto/verify"
    )
    assert response.status_code == 202


def test_verify_signature():
    """
    Test verify signature.
    """
    response = client.get("/crypto/verify?message=hello&signature=hello")
    assert response.status_code == 200


def test_verify_signature_with_cache():
    """
    Test verify signature with cache.
    """
    response = client.get("/crypto/verify?message=hello&signature=hello")
    assert response.status_code == 200

    response = client.get("/crypto/verify?message=hello&signature=hello")
    assert response.status_code == 200
