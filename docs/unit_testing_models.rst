.. _unit_testing_models:

Unit Testing Models
===================

Flaskage includes a variety of powerful tools for testing your models including
model factories and data fakers to easily generate mock objects.

Model Factories
---------------

Using the excellent factory_boy_ library combined with the powerful
fake-factory_, we can generate fake model objects that can be used during
testing.

A factory for each model should be defined in the a file named model_factory.py
in the **tests/fixtures** directory (e.g. blog_post_factory.py).

Here's an example of a factory boy factory that uses fake factory to fake data:

.. code-block:: python

    from app import db
    from app.models import User

    from faker import Factory
    import factory
    from factory.alchemy import SQLAlchemyModelFactory

    fake = Factory.create()

    class UserFactory(SQLAlchemyModelFactory):
        FACTORY_FOR = User
        FACTORY_SESSION = db.session

        username = factory.LazyAttribute(lambda a: fake.user_name())
        email = factory.LazyAttribute(lambda a: fake.email())
        password = factory.PostGenerationMethodCall(
            'set_password', 'password123'
        )

Please see the `factory_boy docs`_ and `fake-factory docs`_ for further
information and examples.

.. _factory_boy: https://github.com/dnerdy/factory_boy
.. _fake-factory: https://pypi.python.org/pypi/fake-factory
.. _factory_boy docs: https://factoryboy.readthedocs.org/en/latest/
.. _fake-factory docs: http://www.joke2k.net/faker/
