import json
from functools import wraps

import redis
from loguru import logger as logger
from redis import StrictRedis
from redisbloom.client import Client

from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg import gcf
encoding = "utf-8"


class RedisOps:
    def __init__(self, params={}):
        self.params = params
        host = self.params.get("redis_host", gcf.redis_host)
        port = self.params.get("redis_port", gcf.redis_port)
        # avoid error when redis server is not available
        with ExceptionCatcher() as ec:
            
            self.r = redis.Redis(host=host, port=port, db=0)
            self.bf = Client(host=host, port=port, db=0)
            self.createdBfNames = set()

    def mget(self, keys=None):
        values = self.r.mget(keys=keys)
        values_ = []
        for value in values:
            if value is not None:
                value = value.decode(encoding)
            values_.append(value)
        return values_

    def mset(self, keydict=None):
        """
        set multi key-value
        :param keydict:
        :return:
        """
        self.r.mset(keydict)

    def set(self, key=None, value=None, ex=None):
        self.r.set(name=key, value=value, ex=ex)

    def get(self, key):
        value = self.r.get(name=key)
        if value is not None:
            value = value.decode(encoding)

        return value

    def lpush(self, key=None, value=None):
        self.r.lpush(key, value)

    def rpop(self, key=None):
        value = self.r.rpop(name=key)
        if value is not None:
            value = value.decode(encoding)

        return value

    def bfPush(self, bfName=None, value=None):
        if bfName in self.createdBfNames:
            self.bf.cfAddNX(bfName, value)
        else:
            try:
                self.bf.cfCreate(bfName, 10000000)

            except BaseException as e:
                logger.debug(
                    "bfName: already existed! will add it to existed set", bfName
                )
                self.createdBfNames.add(bfName)

    def bfExist(self, bfName=None, value=None):
        return self.bf.cfExists(bfName, value)

    def refresh(self, key=None):
        return self.r.expire(key, 1)

    def deleteKey(self, key=None):
        return self.r.delete(key)


redisOps = RedisOps()


def cached(ex=60 * 60 * 24, redisKey=None):
    """
    also key must be compose of kwargs
    result must be json serializable and also dict object
    """

    def cached_real(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate the cache key from the function's arguments.
            key = redisKey
            if key is None:
                args_ = []
                for key, value in kwargs.items():
                    logger.debug("key: {key}, value: {value}", key=key, value=value)
                    args_.append(str(value))

                key_parts = [func.__name__] + args_
                key = "-".join(key_parts)

            result = None
            with ExceptionCatcher() as ec:
                result = redisOps.get(key)

            if result is None:
                # Run the function and cache the result for next time.
                value = func(*args, **kwargs)
                with ExceptionCatcher() as ec:
                    if value is not None:
                        logger.debug("cache key: {key}", key=key)

                        value_json = json.dumps(value)
                        redisOps.set(key=key, value=value_json, ex=ex)

            else:
                logger.info("cache hit: {key}", key=key)

                value = json.loads(result)

            return value

        return wrapper

    return cached_real
