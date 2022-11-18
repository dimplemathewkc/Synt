from app.integration.redis import cache
from app.integration.rabbitmq import queue
from fastapi import APIRouter

router = APIRouter()


def health_check_redis():
    """Check if redis is up."""
    if cache.ping():
        return True
    return False


def health_check_rabbitmq():
    """Check if rabbitmq is up."""
    if queue.is_open:
        return True
    return False


@router.get("/health_check", status_code=200)
def resource_health_check():
    """Check if the application is up."""
    if health_check_redis() and health_check_rabbitmq():
        return True
    return False
