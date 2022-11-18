from app.integration.singleton import Singleton
import pika


@Singleton
class RabbitMQConnection(object):
    """RabbitMQ Connection Class"""

    def __init__(self):
        self.host = "rabbitmq"
        self.port = 5672
        self.user = "guest"
        self.password = "guest"
        self.queue = "fastapi_task"
        self._connection = None

    def get_channel(self):
        """Get RabbitMQ Connection"""
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            self.host, self.port, credentials=credentials
        )
        self._connection = pika.BlockingConnection(parameters)
        channel = self._connection.channel()
        # channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue=self.queue)
        return channel

    def close_connection(self):
        """Close RabbitMQ Connection"""
        self._connection.close()
