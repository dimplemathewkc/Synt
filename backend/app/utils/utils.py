from app.core.config import settings


def make_url(url, message, signature=None):
    """Make a url."""
    if signature is not None:
        return (
            settings.API_URL + url + "?message=" + message + "&signature=" + signature
        )
    return settings.API_URL + url + "?message=" + message
