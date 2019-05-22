import kinto.core
import webtest

from kinto.core.utils import random_bytes_hex
from pyramid.config import Configurator


def get_request_class(prefix):
    class PrefixedRequestClass(webtest.app.TestRequest):
        @classmethod
        def blank(cls, path, *args, **kwargs):
            path = "/%s%s" % (prefix, path)
            return webtest.app.TestRequest.blank(path, *args, **kwargs)

    return PrefixedRequestClass


class BaseWebTest(object):
    """Base Web Test to test your cornice service.

    It setups the database before each test and delete it after.
    """

    api_prefix = "v1"

    def __init__(self, *args, **kwargs):
        super(BaseWebTest, self).__init__(*args, **kwargs)
        self.app = self._get_test_app()
        self.headers = {"Content-Type": "application/json"}

    def _get_test_app(self, settings=None):
        config = self._get_app_config(settings)
        wsgi_app = config.make_wsgi_app()
        app = webtest.TestApp(wsgi_app)
        app.RequestClass = get_request_class(self.api_prefix)
        return app

    def _get_app_config(self, settings=None):
        config = Configurator(settings=self.get_app_settings(settings))
        kinto.core.initialize(config, version="1.0.1")
        return config

    def get_app_settings(self, additional_settings=None):
        """
        kinto.includes = kinto_pusher

        kinto.event_listeners = pusher
        kinto.event_listeners.pusher.use = kinto_pusher.listener
        kinto.event_listeners.pusher.resources = <list of resource names>
        kinto.event_listeners.pusher.channel = <channel-name or pattern>

        pusher.app_id = <pusher-app-id>
        pusher.key = <pusher-key>
        pusher.secret = <pusher-secret>
        """
        settings = kinto.core.DEFAULT_SETTINGS.copy()
        settings["includes"] = "kinto_pusher"
        settings["cache_backend"] = "kinto.core.cache.memory"
        settings["cache_backend"] = "kinto.core.cache.memory"
        settings["userid_hmac_secret"] = random_bytes_hex(16)
        settings["event_listeners"] = "pusher"
        settings["event_listeners.pusher.use"] = "kinto_pusher.listener"
        settings["event_listeners.pusher.resources"] = "records"
        pattern = "{bucket_id}-{collection_id}-{resource_name}"
        settings["event_listeners.pusher.channel"] = pattern
        settings["pusher.app_id"] = "12345"
        settings["pusher.key"] = "demo-key"
        settings["pusher.secret"] = "demo-secret"

        if additional_settings is not None:
            settings.update(additional_settings)
        return settings
