.. _creating:

Creating Your Project
=====================

Now that we have Flaskage environment setup, we can create our first project
and generated some basic boilerplate code using scaffolding.

Creating a New Project
----------------------

To create a new project, simply run the following:

.. code-block:: bash

    $ flaskage new <project_name>

.. note::

    The project name must be in lowercase underscore format, much like regular
    Python variable names.

Alternatively, you may provide a full path to your new application too:

.. code-block:: bash

    $ flaskage new ~/webapps/<project_name>

This will generate a new project structure for you.

Please follow the provided instructions to prepare your project for running.

Once you have completed installing all the necessary components, you may start
the Flask development server using the following command as described in the
instructions:

.. code-block:: bash

    ./manage.py server

This will run the development server on loopback address which will mean that
it will only be available for viewing by your development server.

If you wish to make the website available to other machines on the same
network, then start the development server as follows:

.. code-block:: bash

    ./manage.py server -t 0.0.0.0

Generating Scaffolds
--------------------

A typical Flaskage web application is made up of the following components:

- Blueprints (application components) and their related templates
- Helpers designed to provide utility functions or classes for the application
- Javascript and Stylsheet assets (using Coffeescript and LESS respectively)
  intended to be used for particular blueprints
- Database models
- Libraries designed to provide generic non-application specific utility
  functions or classes for the application and other applications in future

You may generate the required boilerplate code for each of these components
using the **flaskage** command.

Please ensure that you follow all on-screen instructions to activate the new
component in your application.

.. note::

    In all examples below, the name must be in lowercase underscore format.

To generate a new blueprint:

.. code-block:: bash

    flaskage generate blueprint <blueprint_name>

To generate a new helper:

.. code-block:: bash

    flaskage generate helper <helper_name>

To generate a new set of assets:

.. code-block:: bash

    flaskage generate asset <asset_name>

To generate a new model:

.. code-block:: bash

    flaskage generate model <model_name> [<column> <column> ...]

Furthermore, you can specify the columns and their types of your model which
generates the required model code and the respective factory too.  The code
uses a simple system to guess the sort of faker that should be used for the
factory, and so the naming of the columns will alter the outcome.

Each column definition should be specified in the following format::

    <column> ::= <name>[:<type>[,<length>][:<modifier>,<modifier>...]]

- **Name**: The name of the column in lowercase underscore format
- **Type (optional; defaults to string)**: The data type of the column

  - integer (or int)
  - decimal
  - float
  - boolean (or bool)
  - date
  - time
  - datetime
  - binary (or bin)
  - string (or str)
  - text

- **Length (optional; only applies to string, text & binary)**: The required
  length of the column
- **Modifiers (optional)**: Any modifiers relating to the column

  - index
  - primary
  - required
  - unique

.. note::

    If no primary key is specified, a primary key **integer** column named
    **id** will be created for you.

Let's go through an example:

.. code-block:: bash

    flaskage generate model user name:string,100 email:string:index created:datetime

This would generate the following model:

.. code-block:: python

    class User(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        email = db.Column(db.String, index=True)
        created = db.Column(db.DateTime)

And one more example:

.. code-block:: bash

    flaskage generate model person email::primary name::index dob:datetime:required

Notice that I haven't specified **string** explicitly above.  Leaving the type
blank assumes the default type but allows you to then specify modifiers.

This would generate the following model:

.. code-block:: python

    class Person(db.Model, CRUDMixin):
        email = db.Column(db.String, primary_key=True)
        name = db.Column(db.String, index=True)
        dob = db.Column(db.DateTime, nullable=False)

And this time, let's also check out the factory that was generated for us:

.. code-block:: python

    class PersonFactory(SQLAlchemyModelFactory):
        FACTORY_FOR = Person
        FACTORY_SESSION = db.session

        email = factory.LazyAttribute(lambda a: fake.email())
        name = factory.LazyAttribute(lambda a: fake.name())
        dob = factory.LazyAttribute(lambda a: fake.date_time())

Notice how Flaskage chose the correct faker for each column here!

To generate a new library:

.. code-block:: bash

    flaskage generate lib <library_name>

.. note::

    When using the flaskage command, you need not type the full command in
    order to execute it.  In almost all cases, simply typing the first
    letter of the command will suffice.

    For example, the following are equivalent:

    .. code-block:: bash

        flaskage generate blueprint <blueprint_name>
        flaskage g blueprint <blueprint_name>
        flaskage g b <blueprint_name>

