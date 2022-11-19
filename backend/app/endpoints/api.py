from fastapi import APIRouter, Depends, HTTPException
from app.integration.rabbitmq import publish_message
from app.core.config import settings


from app.integration.api_helper import make_request

from app.integration.redis import RedisClient

from backend.app.worker.manager import Manager

router = APIRouter()


@router.get("/crypto/sign")
async def sign_message(message: str, webhook: str):
    """
    This api returns the signature of the message. The api is supported by Redis cache. If the api is unable to get response from api
    the message is stored in the queue and the api returns 202 status code. The api is supported by RabbitMQ queue.
    :param message: message to be signed
    :param webhook: webhook to be called after signing the message
    :return: signature of the message
    """
    redis_client = RedisClient.Instance().get_client()
    if settings.CACHE_ACTIVE:
        if redis_client.get(message) is not None:
            return redis_client.get(message)

    # initiate the manager for single threaded execution
    result = Manager.Instance().process_single_message(message)

    if result is not None:
        if settings.CACHE_ACTIVE:
            redis_client.set(message, result)
        return result

    # if the api is unable to get response from api the message is stored in the queue
    publish_message(message, webhook)

    raise HTTPException(
        status_code=202,
        detail="Your request is being processed, once the result is ready it will be posted to the webhook",
    )


@router.get("/crypto/verify")
def verify_signature(message: str, signature: str):
    """
    The api verifies the signature of the message.
    :param message:
    :param signature:
    :return:
    """
    response = make_request("/crypto/verify", message, signature)
    if response.status_code == 200:
        return {"response": response.text}
    raise HTTPException(status_code=response.status_code, detail=response.text)
