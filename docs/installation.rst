.. _installation:

Installation
============

Flaskage is tested against the most common Linux distributions and Python
versions to ensure seamless usage.  Please follow the steps below to prepare
your operating system and Python environment.

Preparing Your Operating System
-------------------------------

Flaskage supports the following Linux operating systems:

- Debian 6 (Squeeze)
- Debian 7 (Wheezy)
- Ubuntu Server 10.04 LTS (Lucid Lynx)
- Ubuntu Server 12.04 LTS (Precise Pangolin)
- Ubuntu Server 14.04 LTS (Trusty Tahr)
- CentOS 5.x
- CentOS 6.x
- Red Hat Enterprise Linux 5.x
- Red Hat Enterprise Linux 6.x

.. note::

    Although Flaskage is designed to work on Python 3.3 and above, it is
    recommended that you develop projects on Python 2.7 until the Python 3
    ecosystem further matures.

    Python 3 really hasn't presented any compelling advantages over its prior
    version and has added some complexity around aspects of the language which
    many (including me) feel is unnecessary.

You'll need to install some pre-requisites to ensure that all Python packages
install correctly.

If you're running Python 2.6 or 2.7 Debian or Ubuntu Server:

.. code-block:: bash

    $ sudo apt-get install gcc python-dev git

If you're running CentOS 6.x or Red Hat Enterprise Linux 6.x:

.. code-block:: bash

    $ sudo yum install gcc python-devel git

If you're running CentOS 5.x or Red Hat Enterprise Linux 5.x, you'll need to
use the python26 package from EPEL. You may then install required dependencies
as follows:

.. code-block:: bash

    $ sudo rpm -Uvh http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
    $ sudo yum install gcc python26 python26-devel

Preparing Your Python Environment
---------------------------------

Flaskage supports the following Python versions:

- CPython 2.6
- CPython 2.7
- CPython 3.3
- CPython 3.4
- PyPy 2.2

If you haven't already, you'll need to first install setuptools, pip and
virtualenv as follows:

.. code-block:: bash

    $ curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py | sudo python
    $ easy_install pip
    $ pip install virtualenv

Create a virtualenv and install the Flaskage packages:

.. code-block:: bash

    $ mkdir ~/.virtualenv
    $ virtualenv ~/.virtualenv/flaskage
    $ source ~/.virtualenv/flaskage/bin/activate
    $ pip install git+git://github.com/fgimian/flaskage.git

This will make an executable script named **flaskage** available which allows
you to create a new project and generate scaffolding.  More on that to follow
in the next section.

Installing Node.js Components
-----------------------------

In order to use Bower, LESS, Clean CSS, Coffeescript and UglifyJS, we need to
install the necessary modules on our system via Node.js.

Firstly, ensure that your system has the latest Node.js installed and then run
the following:

.. code-block:: bash

    $ [sudo] npm install -g bower less clean-css coffee-script uglify-js

.. note::

    If your Node.js installation is global and owned by root, you'll need to 
    run the command above using sudo.
