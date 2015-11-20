===============================
Cliquet Pusher
===============================

.. image:: https://img.shields.io/travis/leplatrem/cliquet-pusher.svg
        :target: https://travis-ci.org/leplatrem/cliquet-pusher

.. image:: https://img.shields.io/pypi/v/cliquet-pusher.svg
        :target: https://pypi.python.org/pypi/cliquet-pusher

**proof-of-concept**: Plug `Cliquet notifications <http://cliquet.readthedocs.org/en/latest/reference/notifications.html>`_
with `Pusher.com <http://pusher.com>`_.


Install
-------

::

    pip install cliquet-pusher


Setup
-----

In the Cliquet-based application settings:

::

    cliquet.includes = cliquet_pusher

    cliquet.event_listeners = cliquet_pusher.listener
    cliquet.event_listeners.pusher.resources = <list of resource names>
    cliquet.event_listeners.pusher.channel = <channel-name or pattern>

    pusher.app_id = <pusher-app-id>
    pusher.key = <pusher-key>
    pusher.secret = <pusher-secret>


For example, in `Kinto <http://kinto.readthedocs.org/>`_, to be notified of
record updates per collection:

::

    kinto.event_listeners.pusher.resources = record
    kinto.event_listeners.pusher.channel = {bucket_id}-{collection_id}-{resource_name}

> **Note:** *This channel format is the one used in the demo*


TODO
----

- Add view for authenticated channels
