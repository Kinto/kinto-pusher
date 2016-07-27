from kinto.tests.support import unittest
from . import BaseWebTest

from kinto_pusher import __version__ as pusher_version


class CapabilityTestView(BaseWebTest, unittest.TestCase):

    def test_fxa_capability(self, additional_settings=None):
        resp = self.app.get('/')
        capabilities = resp.json['capabilities']
        self.assertIn('pusher', capabilities)
        expected = {
            "version": pusher_version,
            "url": "https://github.com/Kinto/kinto-pusher",
            "description": "Notify Pusher when somethings changes.",
            "app_id": "12345",
            "key": "demo-key"
        }
        self.assertEqual(expected, capabilities['pusher'])
