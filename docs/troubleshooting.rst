.. _troubleshooting:

Troubleshooting
===============

Flaskage comes with several simple helpers for troubleshooting as you develop
your application.

The Shell
---------

A pre-configured shell using the incredible ipython may be invoked using the
following command:

.. code:: bash

    ./manage.py shell

Within this shell, several variables will automatically be made available:

* The Flask application object (app)
* The Flask-SQLAlchemy database object (db)
* All model classes (e.g. User, Post .etc)
* All factory classes (e.g. UserFactory, PostFactory .etc)

The shell is a great place to try out queries or troubleshoot your application.

The Python Debugger
-------------------

TODO

URL Mappings
------------

Unlike frameworks like Django and Rails, Flask allows you to configure your
routing right next to each view which is the preferred way of working in
Flaskage.

However, if you ever wish to see a full mapping of all URLs and their
associated view function, you may run:

.. code:: bash

    ./manage.py urls

Switching Environments
----------------------

Any command that you invoke via manage.py will be run against the development
environment by default.  However, you may easily override this using the **-c**
option as shown below:

.. code:: bash

    ./manage.py -c production shell

This example will run the shell using the production environment.
