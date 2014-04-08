.. _database_design:

Database Queries
================

Now that we've defined our models and used migrations to build our schema,
we're ready to start manipulating our data.

CRUD Operations
---------------

In case you're unaware, CRUD stands for **create, read, update and delete**
which are the common actions one would take with their models.

For any of these operations, be sure to first import the models you require:

.. code-block:: python

    from models import user

To **create** a new record for a model:

.. code-block:: python

    me = User(username='fgimian', name='Fotis')
    me.save()

The auto-generated id will now be avalaible as **me.id**.

To **read** a record using the model's primary key:

.. code-block:: python

    the_user = User.query.get(5)

Further examples of read operations and their respective SQL will follow below.

To **update** a record for a model:

.. code-block:: python

    the_user = User.query.get(5)
    the_user.update(username='newusername')

And finally, to **delete** a record for a model:

.. code-block:: python

    the_user = User.query.get(5)
    the_user.delete()

Select Queries
--------------

If you're like me and love your SQL, you'll understand how frustrating it
can be to use a limited ORM.  Luckily for us, we're using one of the most
powerful ORMs out there and it can do just about anything that raw SQL can do
with its expressive query API.

Selecting all rows in a table

.. code-block:: sql

    SELECT *
    FROM user

translates to:

.. code-block:: python

    users = User.query.all()

Basic filtering

.. code-block:: sql

    SELECT *
    FROM user
    WHERE age = 18

translates to:

.. code-block:: python

    users = User.query.filter_by(age=18)

Obtaining a single record

.. code-block:: sql

    SELECT *
    FROM user
    WHERE username = 'fgimian'
    LIMIT 1

translates to:

.. code-block:: python

    me = User.query.filter_by(username='fgimian').first()

Ordering results

.. code-block:: sql

    SELECT *
    FROM user
    ORDER BY age [DESC]

translates to:

.. code-block:: python

    users = User.query.order_by(User.age)
    users_desc = Userl.query.order_by(User.age.desc())
