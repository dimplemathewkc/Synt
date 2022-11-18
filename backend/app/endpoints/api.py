from fastapi import APIRouter
from app.integration.rabbitmq import send_message
from app.core.config import settings
import redis

from app.integration.api import make_request

router = APIRouter()


@router.get("/crypto/sign", status_code=202)
async def sign_message(message: str, webhook: str):
    """Sign the message."""

    if settings.CACHE_ACTIVE:
        r2 = redis.Redis(host="redis", port=6379, db=1)

        if r2.get(message) is not None:
            return r2.get(message)

    send_message(message, webhook)


@router.get("/crypto/verify")
async def verify_signature(message: str, signature: str):
    """
    Verify a message signature.
    :param message:
    :param signature:
    :return:
    """
    return make_request("/crypto/verify", message, signature)
