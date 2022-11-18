import json
import redis
import pika
import requests
from fastapi import Depends
from app.core.config import settings
from app.integration.redis import cache


def publish_message(message, webhook):
    url = "amqp://guest:guest@rabbitmq:5672"
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP
    channel = connection.channel()
    # channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue="fastapi_task")
    channel.basic_publish(
        exchange="",
        routing_key="fastapi_task",
        body=json.dumps({"message": message, "webhook": webhook}).encode("utf-8"),
    )

    connection.close()
    return


def connect():
    url = "amqp://guest:guest@rabbitmq:5672"
    params = pika.URLParameters(url)
    print(params)
    params.socket_timeout = 5
    print(pika.BlockingConnection(params))
    connection = pika.BlockingConnection(params)

    return connection


def process_message():

    redis_client = redis.Redis(host="redis", port=6379, db=1)

    url = "amqp://guest:guest@rabbitmq:5672"
    params = pika.URLParameters(url)
    params.socket_timeout = 5

    connection = pika.BlockingConnection(params)  # Connect to CloudAMQP

    channel = connection.channel()
    # channel.basic_qos(prefetch_count=1)
    channel.queue_declare(queue="fastapi_task")
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

    connection.close()
