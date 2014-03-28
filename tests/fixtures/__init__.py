# -*- coding: utf-8 -*-
"""
    flaskage.tests.fixtures
    ~~~~~~~~~~~~~~~~~~~~~~~

    Here you can create a number of files each containing a fixture definition
    corresponding to a model definition via factory_boy and fake-factory.

    factory_boy Reference:
    https://factoryboy.readthedocs.org/en/latest/

    fake-factory Reference:
    http://www.joke2k.net/faker/

    A detailed example can be found below to get you started:

    from application import db
    from application.models import User

    from faker import Factory
    import factory
    from factory.alchemy import SQLAlchemyModelFactory

    fake = Factory.create()


    class User(SQLAlchemyModelFactory):
        FACTORY_FOR = User
        FACTORY_SESSION = db.session

        username = factory.LazyAttribute(lambda a: fake.user_name())
        email = factory.LazyAttribute(lambda a: fake.email())
        sex_code = factory.LazyAttribute(
            lambda a: fake.random_int(min=1, max=3))
        password = factory.PostGenerationMethodCall(
            '_set_password', 'defaultpassword')

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
# Import fixtures from the various fixture files so that they are easy to
# import. We also issue a noqa command to avoid flake8's unused import warning.
# from .<submodule> import <fixture>  # noqa
