from redis.asyncio.client import Redis as AsyncRedis
from redis.client import Redis as SyncRedis
from utils import config


async_redis = AsyncRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, password='redispassword$')
sync_redis = SyncRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, password='redispassword$')
