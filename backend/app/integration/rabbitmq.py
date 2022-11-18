import json
import requests
from app.core.config import settings

from app.integration.rabbitmq_conf import RabbitMQConnection

from backend.app.integration.redis import RedisClient


def publish_message(message, webhook):

    channel = RabbitMQConnection.Instance().get_channel()

    channel.basic_publish(
        exchange="",
        routing_key="fastapi_task",
        body=json.dumps({"message": message, "webhook": webhook}).encode("utf-8"),
    )

    RabbitMQConnection.Instance().close_connection()
    return


def process_message():
    redis_client = RedisClient.Instance().get_client()
    channel = RabbitMQConnection.Instance().get_channel()
    # try:
    method_frame, header_frame, body = channel.basic_get(queue="fastapi_task")

    if method_frame is not None:
        message, webhook = json.loads(body.decode("utf-8")).values()

        response = requests.get(
            "https://hiring.api.synthesia.io" + "/crypto/sign?message=" + message,
            headers={"Authorization": "82ca2fe9c123e4437f97b5b29af27751"},
        )
        print(response.status_code)
        if response.status_code == 200:
            if settings.CACHE_ACTIVE:
                print(type(redis_client))
                redis_client.set(message, response.text)
                requests.post(webhook, json={"message": response.text})
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    RabbitMQConnection.Instance().close_connection()
