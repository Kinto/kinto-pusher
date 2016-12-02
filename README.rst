===============================
Kinto Pusher
===============================

.. image:: https://img.shields.io/travis/Kinto/kinto-pusher.svg
        :target: https://travis-ci.org/Kinto/kinto-pusher

.. image:: https://img.shields.io/pypi/v/kinto-pusher.svg
        :target: https://pypi.python.org/pypi/kinto-pusher

Plug `Kinto notifications <http://kinto.readthedocs.io/en/latest/core/reference/notifications.html>`_
into `Pusher.com <http://pusher.com>`_.

* `Online demo <https://kinto.github.io/kinto-pusher/>`_


Install
-------

::

    pip install kinto-pusher

Depending on your environment, it might be necessary to install the `ffi system library <https://sourceware.org/libffi/>`_ with ``sudo apt-get install libffi-dev``.


Setup
-----

In the Kinto-based application settings:

.. code-block:: ini

    kinto.includes = kinto_pusher

    pusher.app_id = <pusher-app-id>
    pusher.key = <pusher-key>
    pusher.secret = <pusher-secret>
    pusher.cluster = eu

    kinto.event_listeners = pusher
    kinto.event_listeners.pusher.use = kinto_pusher.listener

    kinto.event_listeners.pusher.channel = {bucket_id}-{collection_id}-{resource_name}
    kinto.event_listeners.pusher.resources = bucket collection group record
    kinto.event_listeners.pusher.actions = create update delete


TODO
----

- Add view for authenticated channels
