from django.core.cache import cache as DjangoCache
from django.conf import settings
from functools import wraps
from kfsd.apps.models.constants import KEY_CACHE_TIMEOUT


def cache(key):
    def get(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if settings.IS_CACHE_ENABLED:
                data = DjangoCache.get(key)
                if data is None:
                    data = func(*args, **kwargs)
                    DjangoCache.set(key, data, DjangoCache.get(KEY_CACHE_TIMEOUT, 0))
            else:
                data = func(*args, **kwargs)
            return data

        return wrapper

    return get
