import pkg_resources

from pusher import Pusher

#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version


def includeme(config):
    settings = config.get_settings()

    app_id = str(settings['pusher.app_id'])
    key = settings['pusher.key']
    secret = settings['pusher.secret']
    cluster = settings.get('pusher.cluster')

    config.registry.pusher = Pusher(app_id, key, secret, cluster=cluster)

    config.add_api_capability(
        "pusher",
        version=__version__,
        description="Notify Pusher when something changes.",
        url="https://github.com/Kinto/kinto-pusher",
        app_id=app_id,
        key=key)
