import json
from datetime import datetime
import datetime as dt
from backend.app.integration.rabbitmq_conf import RabbitMQConnection
import requests
from core.config import settings
from threading import Thread
from app.integration.redis import RedisClient

from app.integration.singleton import Singleton


@Singleton
class Manager:
    """
    Class Manager is a singleton class that manages the number of concurrent requests to the API.
    It has a list of 10 slots, each slot is a thread that can be used to process a request.
    The class has two methods:
    1. consume_single_message: This method is used to consume a single message from the queue and process it.
    2. process_single_message: This method is used to process a single message and return the result.
    """
    def __init__(self):
        self.clocks = [None] * 10

    def consume_single_message(self):
        """
        This method is used to consume a single message from the queue and process it.
        :return:
        """
        channel = RabbitMQConnection.Instance().get_channel()
        # try:
        method_frame, header_frame, body = channel.basic_get(queue="fastapi_task")

        if method_frame is not None:
            message, webhook = json.loads(body.decode("utf-8")).values()
            free_slots, idx = self.slot_count()
            free_slots = min(free_slots, 5)
            idx = idx[:free_slots]
            results = [None] * free_slots
            threads = [None] * free_slots

            for i in range(free_slots):
                self.clocks[idx[i]] = datetime.now()
                threads[i] = Thread(target=process_request, args=(message, results, i))
                threads[i].start()

            for i in range(free_slots):
                threads[i].join()

            for i in range(free_slots):
                if results[i] is not None:
                    requests.post(webhook, json={"message": results[i]})
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
                    if settings.CACHE_ACTIVE:
                        redis_client = RedisClient.Instance().get_client()
                        redis_client.set(message, results[i])

    def process_single_message(self, message):
        """
        This method is used to process a single message and return the result.
        :param message:
        :return:
        """
        free_slots, idx = self.slot_count()
        if free_slots > 0:
            self.clocks[idx[0]] = datetime.now()
            response = requests.get(
                settings.API_URL + "/crypto/sign?message=" + message,
                headers={settings.API_KEY: settings.API_SECRET},
            )
            if response.status_code == 200:
                return response.text
        return None

    def slot_count(self):
        """
        This method is used to count the number of free slots and return the indices of the free slots.
        :return:
        """
        count = 0
        idx = []
        for _idx, _time in enumerate(self.clocks):
            if _time is None or datetime.now() - _time > dt.timedelta(seconds=60):
                count += 1
                idx.append(_idx)
        return count, idx


def process_request(message, results, idx):
    """
    This function calls the API and stores the result in the results list.
    :param message:
    :param results:
    :param idx:
    :return:
    """
    response = requests.get(
        settings.API_URL + "/crypto/sign?message=" + message,
        headers={settings.API_KEY: settings.API_SECRET},
    )

    if response.status_code == 200:
        results[idx] = response.text
