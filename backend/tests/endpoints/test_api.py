def test_sign_message(client):
    """Test the sign message endpoint."""
    message = "Hello World"
    response = client.get(f"/crypto/sign?message={message}")
    assert response.status_code == 202
    assert response.json() == "Hello World"
