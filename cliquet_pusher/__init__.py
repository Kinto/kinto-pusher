from pusher import Pusher

__author__ = 'Mathieu Leplatre'
__email__ = 'mathieu@leplat.re'
__version__ = '0.1.0'


def includeme(config):
    settings = config.get_settings()

    app_id = str(settings['pusher.app_id'])
    key = settings['pusher.key']
    secret = settings['pusher.secret']

    config.registry.pusher = Pusher(app_id, key, secret)
