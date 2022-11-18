import requests


from app.utils.utils import make_url


from app.core.config import settings


def make_request(url: str, message: str, signature: str):
    """
    Make a request.
    :param url: str
    :param message: str
    :param signature: str
    :return: Response
    """

    url = make_url(url, message, signature)
    return requests.get(url, headers={settings.API_KEY: settings.API_SECRET})
