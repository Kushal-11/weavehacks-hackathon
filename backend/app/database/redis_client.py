import redis.asyncio as redis
import json
from typing import Optional, Any, List
from app.config import settings

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """Connect to Redis"""
        self.redis = redis.from_url(settings.REDIS_URL)
        await self.redis.ping()
    
    async def close(self):
        """Close Redis connection"""
        if self.redis:
            await self.redis.close()
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """Set a key-value pair"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await self.redis.set(key, value, ex=expire)
    
    async def get(self, key: str) -> Any:
        """Get a value by key"""
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.decode('utf-8')
        return None
    
    async def delete(self, key: str):
        """Delete a key"""
        await self.redis.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        return await self.redis.exists(key) > 0
    
    async def lpush(self, key: str, value: Any):
        """Push to left of list"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await self.redis.lpush(key, value)
    
    async def rpop(self, key: str) -> Any:
        """Pop from right of list"""
        value = await self.redis.rpop(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.decode('utf-8')
        return None
    
    async def lrange(self, key: str, start: int = 0, end: int = -1) -> List[Any]:
        """Get range from list"""
        values = await self.redis.lrange(key, start, end)
        result = []
        for value in values:
            try:
                result.append(json.loads(value))
            except json.JSONDecodeError:
                result.append(value.decode('utf-8'))
        return result 