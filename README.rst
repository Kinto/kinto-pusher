===============================
Kinto Pusher
===============================

.. image:: https://img.shields.io/travis/Kinto/kinto-pusher.svg
        :target: https://travis-ci.org/Kinto/kinto-pusher

.. image:: https://img.shields.io/pypi/v/kinto-pusher.svg
        :target: https://pypi.python.org/pypi/kinto-pusher

**proof-of-concept**: Plug `Kinto notifications <http://kinto.readthedocs.io/en/latest/core/reference/notifications.html>`_
into `Pusher.com <http://pusher.com>`_.


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

    kinto.event_listeners = pusher
    kinto.event_listeners.pusher.use = kinto_pusher.listener
    kinto.event_listeners.pusher.resources = <list of resource names>
    kinto.event_listeners.pusher.channel = <channel-name or pattern>

    pusher.app_id = <pusher-app-id>
    pusher.key = <pusher-key>
    pusher.secret = <pusher-secret>


For example, in `Kinto <http://kinto.readthedocs.io/>`_, to be notified of
record updates per collection:

.. code-block:: ini

    kinto.event_listeners.pusher.resources = record
    kinto.event_listeners.pusher.channel = {bucket_id}-{collection_id}-{resource_name}

> **Note:** *This channel format is the one used in the demo*


TODO
----

- Add view for authenticated channels
