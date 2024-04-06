CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

'''
This configuration specifies the backend for Channels layers. 
In this case, it's using an in-memory channel layer, which is useful for development purposes. 
For production, you might want to use a more scalable layer like Redis or another backend.

In this case, it's an in-memory layer, which is useful for development but not suitable for production.
'''