import re

from pyramid.settings import aslist
from cliquet.listeners import ListenerBase


class Listener(ListenerBase):
    def __init__(self, channel, resources):
        super(Listener, self).__init__()
        self.channel = channel
        self.resources = resources

    def __call__(self, event):
        registry = event.request.registry

        resource_name = event.payload['resource_name']
        if self.resources and resource_name not in self.resources:
            return

        channel = self.channel.format(**event.payload)
        channel = re.sub('[^a-zA-Z0-9_\\-]', '', channel)
        action = event.payload['action']

        payload = event.impacted_records

        # XXX: Due to bug in Cliquet 2.11, clean-up payload
        for change in payload:
            if 'old' in change:
                change['old'].pop('__permissions__', None)

        registry.pusher.trigger(channel, action, payload)


def load_from_config(config, prefix=''):
    settings = config.get_settings()

    channel = settings['event_listeners.pusher.channel']
    resources = aslist(settings['event_listeners.pusher.resources'])

    return Listener(channel, resources)
