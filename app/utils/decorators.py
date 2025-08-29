import json
from functools import wraps

from app.init import redis_manager


def generate_key(func, **kwargs) -> str:
    args_str = ":".join(
        f"{k}={v}" for k, v in sorted(kwargs.items()) if isinstance(v, (str, int, float, bool))
    )
    return f"{func.__name__}:{args_str}"


def cache_decorator(expire: int = 60):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            cache_key = generate_key(func, **kwargs)
            cached_data = await redis_manager.get(cache_key)
            if cached_data:
                return json.loads(cached_data)
            result = await func(*args, **kwargs)
            schemas = [f.model_dump() for f in result]
            await redis_manager.set(cache_key, json.dumps(schemas), expire)
            return result

        return inner

    return wrapper
