import redis
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 获取Redis URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 创建Redis连接池
redis_pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)

# 创建Redis客户端
redis_client = redis.Redis(connection_pool=redis_pool)

# 缓存操作类
class RedisCache:
    @staticmethod
    def set(key, value, expire=None):
        """设置缓存"""
        try:
            if expire:
                return redis_client.setex(key, expire, value)
            else:
                return redis_client.set(key, value)
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    @staticmethod
    def get(key):
        """获取缓存"""
        try:
            return redis_client.get(key)
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    @staticmethod
    def delete(key):
        """删除缓存"""
        try:
            return redis_client.delete(key)
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    @staticmethod
    def exists(key):
        """检查缓存是否存在"""
        try:
            return redis_client.exists(key)
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False

    @staticmethod
    def expire(key, seconds):
        """设置缓存过期时间"""
        try:
            return redis_client.expire(key, seconds)
        except Exception as e:
            print(f"Redis expire error: {e}")
            return False

# 创建缓存实例
cache = RedisCache()
