from app.integration.rabbitmq_conf import RabbitMQConnection

def test_rabbitmq():
    """Test RabbitMQ connection."""
    rabbitmq = RabbitMQConnection.Instance()
    channel = rabbitmq.get_channel()
    assert channel is not None
