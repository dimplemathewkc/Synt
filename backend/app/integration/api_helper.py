import requests
from app.core import settings

from app.utils.utils import make_url


def make_request(url, message, signature=None):
    """Make a request."""
    url = make_url(url, message, signature)

    return requests.get(url, headers={settings.API_KEY: settings.API_SECRET})
