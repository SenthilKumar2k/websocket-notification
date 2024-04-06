# Install Django Channels and Redis
pip install channel-redis

# In your Django project's settings.py, add the following:
INSTALLED_APPS = [
    # ...
    'channels',
]

ASGI_APPLICATION = 'project_name.routing.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}