from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app.integration.rabbitmq import process_message
from app.core.config import settings

from app.endpoints import api

from app.worker.manager import Manager


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    _app.include_router(api.router)
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
async def ping_api():
    """

    :return:
    """
    try:

        Manager.Instance().consume_single_message()
    except Exception as e:
        print(e)
