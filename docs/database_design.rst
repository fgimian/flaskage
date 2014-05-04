.. _database_design:

Database Design
===============

Flaskage leverages the extremely powerful SQLAlchemy_ ORM for database
interaction.  SQLAlchemy can indeed by a little overwhelming when starting
out, but it's worth it in the long run.

In most cases, it is suggested that you use scaffolding to generate your models
so that they are created in the correct location and with the correct
Flaskage naming conventions which have been carefully thought out.  However,
this page goes through all details of manual model design so that you can
understand how everything works.

The CRUD Mixin
--------------

Unlike Django's ORM, SQLAlchemy has a slightly lower level API whereby updating
records requires them to be added to a session and then the session committed.

Enter the **CRUDMixin** which provides some handy helpers that you can use
on all your models.  These include create, update, save and delete methods.

We'll be using the CRUDMixin in the examples that follow but use of this base
class is entirely optional.

Model Definitions
-----------------

It is recommended that you create one file per model in the models directory
named the same name as the model in lowercase underscore notation.

All model class names and their related filename should be **singular**.  For
example, the model class named **BlogPost** should be in a file named
**blog_post.py**.

So let's look at a basic model definition:

.. code-block:: python

    from datetime import datetime

    from .. import db
    from . import CRUDMixin

    class User(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=False, unique=True)
        email = db.Column(db.String(100), unique=True)
        creation_date = db.Column(db.DateTime, default=datetime.utcnow)

So here, we demonstrate the main directives used when defining models using
SQLAlechmy with Flask.

.. note::

    - When defining models with SQLAlchemy, you must explicitly create a
      primary key for each table (which usually will be named id and similar to
      the example above).
    - In SQLAlchemy, columns are nullable by default which means that null
      values are allowed.  If you wish to specify that the column must include
      a value at all times, then be sure to set nullable to False as we have
      here with the username.
    - The default keyword argument takes in a callable function which generates
      the default value for a column if not specified by the user.

Once you have defined your models, you must register them in
**app/models/__init__.py** by importing them in the following manner:

.. code-block:: python

    from .user import User  # noqa

This enables database migrations for the new model and makes it easier to
import in views.  The **noqa** directive in the comments tells Flake8
to ignore the import as it would otherwise raise a warning stating that the
model was unused in that file.

Please see `SQLAlchemy Declarative Documentation`_ for more information.

Let's go through other column types that you'll commonly use in models:

.. code-block:: python

    class MyModel(db.Model, CRUDMixin):
        boolean_column = db.Column(db.Boolean)
        decimal_column = db.Column(db.Numeric)
        float_column = db.Column(db.Float)
        integer_column = db.Column(db.Integer)
        text_column = db.Column(db.Text)

Please see `SQLAlchemy Column and Data Types Documentation`_ for more
information.

Relationship Definitions
------------------------

.. note::

    At the current time, Flaskage scaffolding doesn't support creation of
    relationships, so the foreign key fields and relationships will need to be
    added manually after you generate the model with all other fields.

**One to many** relationships may be defined as follows:

.. code-block:: python

    # Category table (in app/models/category.py)
    class Category(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))

    # Post table (in app/models/post.py)
    class Post(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        body = db.Column(db.Text)
        pub_date = db.Column(db.DateTime, default=datetime.utcnow)

        # One to many relationship
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        category = db.relationship('Category', backref=db.backref('posts'))

The **backref** property specifies the member variable that will be used to
access the related posts when working with a Category object.

For example:

.. code-block:: python

    chosen_category = Category.get_by_id(5)
    posts_in_category = chosen_category.posts

The relationship may also be specified on the other end if you like:

.. code-block:: python

    # Category table (in app/models/category.py)
    class Category(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
        posts = db.relationship('Post', backref=db.backref('category'))

    # Post table (in app/models/post.py)
    class Post(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        body = db.Column(db.Text)
        pub_date = db.Column(db.DateTime, default=datetime.utcnow)

        # One to many relationship
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

**Many to many** relationships may be defined as follows:

.. code-block:: python

    # User table (in app/models/user.py)
    class User(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=False, unique=True)
        email = db.Column(db.String(100), unique=True)

    # Relationship table (in app/models/relationships.py)
    users_posts = db.Table(
        'users_posts',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

    # Post table (in app/models/post.py)
    class Post(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        ...
        # Many to many relationship
        users = db.relationship(
            'User', secondary=users_posts, backref=db.backref('posts')
        )

All many to many relationship tables should be placed in the file
**relationships.py** under the **app/models** directory.

**One to one relationships** are achieved using the **uselist** flag as shown
below:

.. code-block:: python

    class User(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
        profile = db.relationship('Profile', db.backref=('user', uselist=False))

    class Profile(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)

Alternatively, the relationship may be reversed:

.. code-block:: python

    class User(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        profile = db.relationship('Profile', uselist=False, backref='user')

    class Profile(db.Model, CRUDMixin):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

Please see `SQLAlchemy Relationship Configuration Documentation`_ for more
information.

Database Migrations
-------------------

Thanks to alembic_ and the Flask-Migrate_ extension, Flaskage implements the
ability to easily alter the database schema as the application evolves over
time.

Each time you update or add models, you can generate a new migration by running
the following in the root directory of your project:

.. code-block:: bash

    ./manage.py db migrate

This introspects the database and generates a new migration which will be
placed in the **db/migrations** directory.  Carefully review the migration to
verify that it is correct and then update your database as follows:

.. code-block:: bash

    ./manage.py db upgrade

Changes may be undone by downgrading the migration:

.. code-block:: bash

    ./manage.py db downgrade

.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _SQLAlchemy Declarative Documentation: http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative.html
.. _SQLAlchemy Column and Data Types Documentation: http://docs.sqlalchemy.org/en/latest/core/types.html
.. _SQLAlchemy Relationship Configuration Documentation: http://docs.sqlalchemy.org/en/latest/orm/relationships.html
.. _alembic: https://pypi.python.org/pypi/alembic
.. _Flask-Migrate: https://github.com/miguelgrinberg/Flask-Migrate
