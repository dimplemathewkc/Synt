import redis
from fastapi import APIRouter, Depends
from app.integration.rabbitmq import publish_message
from app.core.config import settings
from app.integration.redis import cache

from app.integration.api_helper import make_request
from pydantic import BaseModel

router = APIRouter()


@router.get("/crypto/sign", status_code=202)
async def sign_message(
    message: str, webhook: str, redis_client: redis.Redis = Depends(cache)
):
    """
    The API endpoin forwards the request to hiring api. This is encapsulated in a task
    that runs in the background. To intiate the task the message is added the queue and
    the last keeps listening to the queue and makes request to the external api and once the result is retrieved the
    response is posted back to the webhook.

    :param message: client message
    :param webhook: callqack url
    :param redis_client: dependency
    :return:
    """

    if settings.CACHE_ACTIVE:
        if redis_client.get(message) is not None:
            return redis_client.get(message)

    publish_message(message, webhook)


@router.get("/crypto/verify")
def verify_signature(message: str, signature: str):
    """
    Verify a message signature.
    :param message:
    :param signature:
    :return:
    """
    response = make_request("/crypto/verify", message, signature)

    return {"response": response.text}
