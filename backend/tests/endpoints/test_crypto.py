from backend.app.endpoints import crypto


def test_sign():
    """Test signing a message."""
    message = "This is a message"
    signature = crypto.sign_message(message)
    assert signature is not None


# def test_verify():
#     """Test verifying a message signature."""
#     message = "This is a message"
#     signature = crypto.sign_message(message)
#     assert crypto.verify_signature(message, signature)
