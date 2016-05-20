========
Run Demo
========

This demo uses *Kinto*, the quintessential "Kinto-based application".

The objective of this tutorial is to run `this demo <http://leplatrem.github.io/kinto-pusher/>`_
using a local server.

We will run *Kinto* locally with this plugin enabled, and observe live sync
between two browsers.


Setup a Pusher account
----------------------

* Go to `Pusher.com <http://pusher.com/>`_
* Create a new app
* Get your app credentials (``app_id``, ``key``, ``secret``)


Run Kinto locally
-----------------

Follow `the instructions in Kinto documentation <http://kinto.readthedocs.io>`_,
but roughly it should be:

::

    $ pip install kinto
    $ kinto init
    $ kinto migrate
    $ kinto start

* It should run on http://localhost:8888

* Follow the instructions of this plugin to install and set the appropriate settings
  in ``config/kinto.ini``

It should reload the new config automatically.


Test Pusher events
------------------

Now that *Kinto* runs locally and is configured to send events to *Pusher*, you
should be able to see them in the *Debug Console* of your *Pusher dashboard*.

For example, create an arbitrary record with `cURL <https://en.wikipedia.org/wiki/CURL>`_

::

    curl -i --user alice:secret -H "Content-Type: application/json" \
         -X POST -d '{"data":{"name":"bob"}}' \
         http://localhost:8888/v1/buckets/default/collections/tasks/records

This created a record, and you should see the generated event in the dashboard.


Run the webpage
---------------

* Replace ``<Pusher key>`` by your ``key`` in the ``demo/map.js`` file
* Run locally:

::

    cd demo/
    python -m SimpleHTTPServer 9999

* Navigate to http://localhost:9999 with two browsers, create and move markers in order to observe live sync!


Going further
-------------

The whole live sync demo is contained in the ``setupLiveSync()`` function.

Of course, *Kinto* (and *kinto.js*) were just an example.

You can use the *Pusher* libraries and SDK in your Web/mobile applications to
receive notifications from any *Kinto*-based service in any kind of
platform.
