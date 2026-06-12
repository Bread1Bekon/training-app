from config import settings
from redis import asyncio as aioredis
import json
from functools import wraps


redis_db = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,
)


def cache_decorator(expire: int = 86400):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # нормализация значения аргументов
            arg_vals = []

            def get_stable_repr(val):
                if val is None:
                    return "None"
                if isinstance(val, (int, float, bool, str)):
                    return str(val)
                if hasattr(val, "model_dump"):
                    return json.dumps(val.model_dump(), sort_keys=True)
                if hasattr(val, "dict"):
                    return json.dumps(val.dict(), sort_keys=True)
                if isinstance(val, (list, tuple, set)):
                    return "[" + ",".join(get_stable_repr(item) for item in val) + "]"
                if isinstance(val, dict):
                    return "{" + ",".join(f"{k}:{get_stable_repr(v)}" for k, v in sorted(val.items())) + "}"

                val_repr = repr(val)
                if "object at" in val_repr or "0x" in val_repr:
                    return val.__class__.__name__
                return val_repr

            for arg in args:
                arg_vals.append(get_stable_repr(arg))
            for k, v in sorted(kwargs.items()):
                arg_vals.append(f"{k}={get_stable_repr(v)}")

            args_str = "-".join(arg_vals)
            # Use a prefix to keep keys neat in Redis
            cache_key = f"cache:{func.__name__}:{args_str}"

            try:
                cached_data = await redis_db.get(cache_key)
                if cached_data is not None:
                    try:
                        return json.loads(cached_data)
                    except Exception:
                        return cached_data
            except Exception as e:
                print(f"Redis get cache failed: {e}")

            result = await func(*args, **kwargs)

            if result is not None:
                try:
                    def make_serializable(data):
                        if isinstance(data, list):
                            return [make_serializable(item) for item in data]
                        if isinstance(data, dict):
                            return {k: make_serializable(v) for k, v in data.items()}
                        if hasattr(data, "model_dump"):
                            return data.model_dump()
                        if hasattr(data, "dict"):
                            return data.dict()
                        return data

                    serialized_result = make_serializable(result)
                    await redis_db.setex(cache_key, expire, json.dumps(serialized_result))
                except Exception as e:
                    print(f"Redis set cache failed: {e}")

            return result

        return wrapper

    return decorator