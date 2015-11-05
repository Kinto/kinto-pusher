import re

from pyramid.settings import aslist
from cliquet.listeners import ListenerBase


class Listener(ListenerBase):
    def __init__(self, channel, resources):
        super(Listener, self).__init__()
        self.channel = channel
        self.resources = resources

    def __call__(self, event):
        resource_name = event.payload['resource_name']
        if self.resources and resource_name not in self.resources:
            return

        channel = self.channel.format(**event.payload)
        channel = re.sub('[^a-zA-Z0-9_\\-]', '', channel)
        action = event.payload['action']

        pusher = event.request.registry.pusher
        pusher.trigger(channel, action, event.payload)


def load_from_config(config):
    settings = config.get_settings()

    channel = settings['event_listeners.pusher.channel']
    resources = aslist(settings['event_listeners.pusher.resources'])

    return Listener(channel, resources)
