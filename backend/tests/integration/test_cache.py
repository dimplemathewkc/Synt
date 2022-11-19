from app.integration.redis import RedisConnection

def test_redis():
    """Test Redis connection."""
    redis = RedisConnection.Instance()
    assert redis is not None
