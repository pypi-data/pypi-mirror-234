

def apply_patches():
    from . import kombu
    from . import redis

    kombu.apply_patch()
    redis.apply_patch()
