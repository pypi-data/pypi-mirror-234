from time import time

try:
    from redis import asyncio as aioredis
    import redis
    _has_redis = True
except ImportError:
    _has_redis = False

if _has_redis:
    class RedisDB:
        def __new__(self, *, asyncio=False, host="localhost", port=6379, db=0, decode_responses=True, **kwargs):
            if asyncio:
                return BaseAIORedis(host=host, port=port, db=db, decode_responses=decode_responses, **kwargs)
            else:
                return BaseRedis(host=host, port=port, db=db, decode_responses=decode_responses, **kwargs)

    class BaseAIORedis(aioredis.Redis):
        def __init__(self, *args, decode_responses=True, **kwargs):
            super().__init__(*args, decode_responses=decode_responses, **kwargs)
        
        @classmethod
        @property
        def current_timestamp(self):
            return int(time())
        

    class BaseRedis(redis.StrictRedis):
        def __init__(self, *args, decode_responses=True, **kwargs):
            super().__init__(*args, decode_responses=decode_responses, **kwargs)
            
        @classmethod
        @property
        def current_timestamp(self):
            return int(time())