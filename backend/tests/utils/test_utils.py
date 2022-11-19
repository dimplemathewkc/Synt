# test api helper
from app.utils.utils import make_url


def test_make_url():
    """
    Test make request.
    """
    url = make_url('http://localhost:5000', 'message', 'signature')
    assert url == 'https://hiring.api.synthesia.iohttp://localhost:5000?message=message&signature=signature'
