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
    assert response.status_code in (200, 202)


def test_sign_message_with_cache():
    """
    Test sign message with cache.
    """
    response = client.get(
        "/crypto/sign?message=hello&webhook=http://localhost:8000/crypto/verify"
    )
    assert response.status_code in (200, 202)

    response = client.get(
        "/crypto/sign?message=hello&webhook=http://localhost:8000/crypto/verify"
    )
    assert response.status_code in (200, 202)


def test_verify_bad_signature():
    """
    Test verify signature.
    """
    response = client.get("/crypto/verify?message=hello&signature=hello")

    assert response.status_code == 400

def test_verify_with_good_signature():
    """
    Test verify signature.
    """
    response = client.get("/crypto/verify?message=hellyuuppni&signature=IsxjEuZekJEKXn3o8GZlXCG_U2ZAFdlyjIuE-_a4-JEv1OT-vCzbIW6OKM1-whD3_vnS15_CbSf0nCXZIvq5c5m9TeQVk8bXKgjGsCqldBibQ9l32BNANXjHXChc6OlfktG7edJNSDjqVvlxyKjhESf59akDFYRtRa3KpwpTr74RqEW_VnJT_6hLqRZTDJDRlC8-clgdOY_dJFTbLT10MHRhcTCKh6edZe03cEaSmzrLvN779DpmcxOFB3UuWzhtm9XZbyrfKooP5V92aowNWtfdADpJ32DREEbRe5sOJXMRCb2GdaVDKz4VI4Ak0j18R06uE-y-CmSK1habjVjFGg==")
    assert response.status_code == 200
