# test api helper
def test_api_helper():
    """
    Test api helper.
    """
    from app.integration.api_helper import make_request

    url = "/crypto/sign"
    message = "hello"
    signature = "hello"
    response = make_request(url, message, signature)
    assert response.status_code == 200
