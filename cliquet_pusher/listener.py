import re

from pusher import Pusher
from cliquet.listeners import ListenerBase


class Listener(ListenerBase):
    def __init__(self, app_id, key, secret, channel=None):
        super(Listener, self).__init__()
        self.pusher = Pusher(app_id, key, secret)
        self.channel = '{bucket_id}-{collection_id}'

    def __call__(self, event):
        resource_name = event.payload['resource_name']
        if resource_name != 'record':
            return

        action = event.payload['action']
        channel = self.channel.format(**event.payload)
        channel = re.sub('[^a-zA-Z0-9_\\-]', '', channel)
        self.pusher.trigger(channel, action, event.payload)


def load_from_config(config):
    settings = config.get_settings()
    app_id = str(settings['event_listeners.pusher.app_id'])
    key = settings['event_listeners.pusher.key']
    secret = settings['event_listeners.pusher.secret']
    return Listener(app_id, key, secret)
