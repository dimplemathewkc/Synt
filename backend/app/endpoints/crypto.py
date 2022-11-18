from fastapi import APIRouter
import requests
from core.config import settings
import time
import redis

router = APIRouter()



@router.get("/crypto/sign")
async def sign_message(message: str, webhook: str):
    """Sign the message."""
    r = redis.Redis(host='redis', port=6379, db=0)
    r2 = redis.Redis(host='redis', port=6379, db=1)

    if r2.get(message) is not None:
        return r2.get(message)

    if r.get(webhook) is None:
        r.set(webhook, message)
    elif r.get(webhook) is not None and r.get(webhook) != message:
        r.set(webhook + str(time.time()), message)
    else:
        pass


    return 202





# @router.get("/crypto/verify")
# async def verify_signature(message: str, signature: str):
#     """
#     Verify a message signature.
#     :param message:
#     :param signature:
#     :return:
#     """
#     return {"message": message, "signature": signature}
