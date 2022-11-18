import redis


redis_conf = {
    "host": "redis",
    "port": 6379,
    "db": 1,
    "charset": "utf-8",
    "decode_responses": True,
}


def cache():
    conn = redis.Redis(**redis_conf)
    try:
        yield conn
    except Exception as e:
        print(e)
    finally:
        conn.close()
