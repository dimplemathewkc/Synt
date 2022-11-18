from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import redis
from fastapi_utils.tasks import repeat_every

from core.config import settings

from endpoints import crypto


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.include_router(crypto.router)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

@app.on_event("startup")
@repeat_every(seconds=1, wait_first=False, raise_exceptions=True)
def ping_api():
    """Ping the API."""
    r = redis.Redis(host='redis', port=6379, db=0, charset="utf-8", decode_responses=True)
    r2 = redis.Redis(host='redis', port=6379, db=1, charset="utf-8", decode_responses=True)
    if len(r.keys()) > 0:
        print('hello edilson')
        key = r.keys()[0]
        message = r.get(key)
        response = requests.get("https://hiring.api.synthesia.io/" + "/crypto/sign?message=" + message,
                                headers={"Authorization": "82ca2fe9c123e4437f97b5b29af27751"})
        if response.status_code == 200:
            r.delete(key)
            r2.set(message, response.text)
