===============================
Cliquet Pusher
===============================

.. image:: https://img.shields.io/travis/leplatrem/cliquet_pusher.svg
        :target: https://travis-ci.org/leplatrem/cliquet_pusher

.. image:: https://img.shields.io/pypi/v/cliquet_pusher.svg
        :target: https://pypi.python.org/pypi/cliquet_pusher

Plug Cliquet notifications with Pusher.com

Install
-------

::

    pip install cliquet_pusher


Setup
-----

In the Cliquet-based application settings:

::

    cliquet.includes = cliquet_pusher

    cliquet.event_listeners = cliquet_pusher.listener
    cliquet.event_listeners.pusher.app_id = <pusher-app-id>
    cliquet.event_listeners.pusher.key = <pusher-key>
    cliquet.event_listeners.pusher.secret = <pusher-secret>


TODO
----

* Add view for authenticated channels
