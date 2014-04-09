.. database_queries:

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

    from models import User

To **create** a new record for a model:

.. code-block:: python

    me = User(username='fgimian', name='Fotis')
    me.save()

The auto-generated id will now be avalaible as **me.id**.

To **read** a record using the model's primary key:

.. code-block:: python

    the_user = User.query.get(5)

Further examples of read operations (select queries) and their respective SQL
will follow below.

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

    users = User.query.filter_by(age = 18).all()

You may also filter using other standard <, >, != operators:

.. code-block:: sql

    SELECT *
    FROM user
    WHERE age < 18
    AND age >= 5

translates to:

.. code-block:: python

    users = User.query.filter((User.age < 18) & (User.age >= 5)).all()

Obtaining a single record

.. code-block:: sql

    SELECT *
    FROM user
    WHERE username = 'fgimian'
    LIMIT 1

translates to:

.. code-block:: python

    me = User.query.filter_by(username = 'fgimian').first()

The **first** function will return **None** if no records were found.  In the
case that multiple records are found matching your filter, only the first row
will be returned.

To ensure that only a single result is present

.. code-block:: sql

    SELECT *
    FROM user
    WHERE username = 'fgimian'

translates to:

.. code-block:: python

    me = User.query.filter_by(username = 'fgimian').one()

The **one** function will return a single row, however it will raise a
**sqlalchemy.orm.exc.NoResultFound** exception if no records were found or a
**sqlalchemy.orm.exc.MultipleResultsFound** exception if multiple records were
found.

Filtering using an in statement:

.. code-block:: sql

    SELECT *
    FROM user
    WHERE username IN ('fgimian', 'lonelycat')

translates to:

.. code-block:: python

    users = User.query.filter(User.username.in_(['fgimian', 'lonelycat'])).all()

Selecting particular columns only

.. code-block:: sql

    SELECT username, email
    FROM user

translates to:

.. code-block:: python

    users = User.query.with_entities(User.username, User.email).all()

.. note::

    Using the **with_entitities** function returns a list of tuples instead
    of a list of objects as per the other queries.

Logical operators for use with filtering:

.. code-block:: sql

    SELECT *
    FROM user
    WHERE (username = 'fgimian'
           OR username = 'lonelycat')
    AND id < 3

.. code-block:: python

    users = User.query.filter(
        (User.username == 'fgimian') | (User.username == 'lonelycat') &
        (User.id < 3)
    ).all()

Applying functions to columns when selecting

.. code-block:: sql

    SELECT upper(username)
    FROM user

.. code-block:: python

    users = User.query.with_entities(db.func.upper(User.username)).all()

Ordering results

.. code-block:: sql

    SELECT *
    FROM user
    ORDER BY age [DESC]

translates to:

.. code-block:: python

    users = User.query.order_by(User.age)
    users_desc = User.query.order_by(User.age.desc())

Grouping by

.. code-block:: sql

    SELECT age, count(*)
    FROM user
    GROUP BY age
    HAVING count(*) > 5

translates to:

.. code-block:: python

    users = User.query.with_entities(
        User.age, db.func.count()
    ).group_by(User.age).having(db.func.count() > 5).all()

Aliasing columns

.. code-block:: sql

    SELECT age, count(*) AS counter
    FROM user
    GROUP BY age
    HAVING counter > 5

translates to:

.. code-block:: python

    users = User.query.with_entities(
        User.age, db.func.count().label('counter')
    ).group_by(User.age).having('counter > 5').all()
