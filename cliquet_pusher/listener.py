import re

from pyramid.settings import aslist
from pyramid.exceptions import ConfigurationError
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

        payload = event.impacted_records

        pusher = event.request.registry.pusher
        pusher.trigger(channel, action, payload)


def load_from_config(config):
    settings = config.get_settings()

    if not hasattr(config.registry, 'pusher'):
        error_msg = ("'cliquet_pusher' seems to be missing from "
                     "%s.includes" % settings['project_name'])
        raise ConfigurationError(error_msg)

    channel = settings['event_listeners.pusher.channel']
    resources = aslist(settings['event_listeners.pusher.resources'])

    return Listener(channel, resources)
