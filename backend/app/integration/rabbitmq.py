import json
import requests
from app.core.config import settings

from app.integration.rabbitmq_conf import RabbitMQConnection

from backend.app.integration.redis import RedisClient


def publish_message(message, webhook):
    """
    This method is used to publish a message to the queue.
    :param message: client message
    :param webhook: client webhook
    :return:
    """
    channel = RabbitMQConnection.Instance().get_channel()

    channel.basic_publish(
        exchange="",
        routing_key="fastapi_task",
        body=json.dumps({"message": message, "webhook": webhook}).encode("utf-8"),
    )

    RabbitMQConnection.Instance().close_connection()
    return
