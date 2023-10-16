__all__ = ('apply_patch', )


def apply_patch():
    from kombu import transport

    transport.TRANSPORT_ALIASES.update({
      'redis-cluster': 'celery.patches.kombu.redis_cluster:Transport',
    })
