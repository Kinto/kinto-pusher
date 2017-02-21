import re

from kinto.core.listeners import ListenerBase


class Listener(ListenerBase):
    def __init__(self, channel, *args, **kwargs):
        super(Listener, self).__init__(*args, **kwargs)
        self.channel = channel

    def __call__(self, event):
        try:
            channel = self.channel.format(**event.payload)
        except KeyError:
            # In case we cannot build the channel name with the
            # current event just ignore it. Refs #19
            return

        channel = re.sub('[^a-zA-Z0-9_\\-]', '', channel)
        action = event.payload['action']

        payload = event.impacted_records

        registry = event.request.registry
        try:
            registry.pusher.trigger(channel, action, payload)
        except ValueError:
            # In case pusher refuse to send large payload try without
            # payload.
            payload = {"payload": "Too large to be sent from there."}
            registry.pusher.trigger(channel, action, payload)


def load_from_config(config, prefix=''):
    settings = config.get_settings()

    # XXX: this will only work if configured listener is called `pusher`
    channel = settings.get('event_listeners.pusher.channel',
                           '{bucket_id}-{collection_id}-{resource_name}')

    return Listener(channel)
