.. _configuring:

Configuring Your Project
========================

Flaskage makes it easy to maintain a hierarchical configuration that can work
in each of your environments.  The base class named **Config** is common
across all environments.  Classes which inherit from this object can then
define certain customisations which relate to each specific site.

Generating Secret Keys
----------------------

Open **config.py** and start by generating some good secret keys for each of
your environments.  To do this, simply open a Python shell and run the
following several times to generate multiple secret keys.

   >>> import os
   >>> os.urandom(24)

Place the contents of each randomly generated key in the **SECRET_KEY**
config parameter for each environment.

Database Configuration
----------------------

Next up, configure your database via the **SQLALCHEMY_DATABASE_URI** variable.
Please find several examples below:

For **PostgreSQL**:

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@host/dbname'

You'll need to install the `psycopg2 <https://pypi.python.org/pypi/psycopg2>`_
package to enable this database.

.. code-block:: bash

    pip install psycopg2

.. note::

    In general, PostgreSQL provides superior performance and features to MySQL
        and is therefore the preferred database for use with Flaskage.

For **MySQL**:

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@host/dbname'

You'll need to install the `MySQL-python <https://pypi.python.org/pypi/MySQL-python>`_
package to enable this database.

.. code-block:: bash

    pip install MySQL-python

For **SQLite**:

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(Config.PROJECT_ROOT, 'dbname.db'))

Please ensure that you add any newly installed package in your
**requirements.txt** file.  You may list your installed packages as follows:

.. code-block:: bash

    pip freeze

Managing Configuration Environments
-----------------------------------

As you'll notice, by default Flaskage provides a production, development and
testing configuration out of the box.

If you would like to add an additional configuration environment, simply
create a new class which inherits from **Config** similar to that below:

.. code-block:: python

    class StagingConfig(Config):
        SQLALCHEMY_DATABASE_URI = 'postgresql://flaskage:pass123@localhost/stagingdb'

You'll then need to add the config to the **AVAILABLE_CONFIGS** global dict
so that it may be used.

.. code-block:: python

    AVAILABLE_CONFIGS = {
        'production': 'config.ProductionConfig',
        'development': 'config.DevelopmentConfig',
        'testing': 'config.TestingConfig',
        'staging': 'config.StagingConfig'
    }

While running the development server, a default configuration is loaded if
not specified by the user.  You may change the default config by updating the
**DEFAULT_CONFIG** global variable as shown below:

.. code-block:: python

    DEFAULT_CONFIG = 'staging'
