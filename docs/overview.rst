.. _overview:

Overview
========

Flaskage incorporates a large number of features and integrates almost
everything you will ever need to build a large web application.

Features
--------

So what makes Flaskage unique? A few little things:

- **Clean and simple**: Although I'm designing Flaskage for medium to larger
  sized projects, I wanted to ensure that the boilerplate code was kept to a
  minimum.  Instead, I've opted for comments which provide examples of what
  you can do rather than starting to write an application in the template.
- **One directory per function**: It seems that most templates are inspired
  by the way that Django separates apps, whereby each component of the larger
  web application has its own models, views, templates and static files.  I
  personally feel that this layout doesn't make sense.  Instead, I prefer a
  structure more similar to the Play_ or `Ruby on Rails`_ which keeps views
  in one directory, models in one directory and so on.  The ability to split
  views and models into multiple files is an absolute must which is also part
  of Flaskage's design.
- **Full integration of Flask-Assets**: This template has been designed for
  use with Coffeescript, LESS (in particular Twitter's Bootstrap CSS framework)
  or any other pre-processor you may have in mind.  Furthermore, Flaskage keeps
  all such uncompiled files neatly in an assets directory.
- **Database migrations**: Flaskage integrates Flask-Migrate_ and is
  ready for database migrations which can be invoked via management commands.
- **PyJade integration**: If you choose to, you may use PyJade_ to write your
  templates.  This is a far less verbose language than regular HTML.
- **Switchable configurations**: With a simple command line switch, you can
  run the development server under any environment you wish (development,
  production or testing).  Further to this, you can set a default environment
  for your app to run in via a variable in the config module or define your
  own custom config environments.
- **Flake8 integration**: You can check that your syntax is valid and that
  your coding style follows the PEP8 standard with a simple management command.
- **Clean client-side library integration**: Flaskage uses Bower and symlinks
  to cleanly integrate Twitter Bootstrap and jQuery with the ability to
  seamlessly upgrade these components when necessary and avoid duplication of
  the original source code in your Git repository.
- **More robust development server**: Using flask-failsafe_, the development
  server won't crash each time small errors are made while coding.
- **Travis Integration**: Test case integration with Travis is provided out
  of the box.
- **Powerful test tools**: Integrated use of nose_, Coverage.py_, factory_boy_
  and fake-factory_.
- **Behaviour-driven development**: Integrated use of behave_, splinter_ and
  selenium_ for fully featured behaviour-driven development.
- **Python 3 ready**: I have only chosen extensions which work across
  Python 2.6, 2.7 and 3.3 so that you're future-proof if and when you decide
  to move to a Python 3 environment.

Project Structure
-----------------

Flaskage is structured as shown below::

    |-- app
    |   |-- assets
    |   |-- models
    |   |-- static
    |   |-- templates
    |   |-- vendor
    |   '-- views
    |-- db
    |   '-- migrations
    |-- docs
    |-- features
    |   '-- steps
    |-- lib
    |-- tests
    |   |-- fixtures
    |   |-- lib
    |   |-- models
    |   '-- views
    |-- bower.json
    |-- config.py
    |-- manage.py
    |-- setup.cfg
    '-- requirements.txt

The purpose of each file and directory are as follows:

- **app**: Main web application directory with app initialisation

  - **assets**: Pre-compiled script and stylsheet assets
  - **models**: Database model definitions
  - **static**: Static files such as CSS, Javascript and images
  - **templates**: Jinja2 templates for presentation
  - **vendor**: Vendor provided script and stylesheet assets
  - **views**: Views and related forms that provide business logic for each page

- **db**: Database related code and binaries

  - **migrations**: The generated Alembic database migrations

- **docs**: Sphinx project documentation
- **features**: Feature definitions in the Gherkin language to be used for BDD

  - **steps**: Test code which validates that each feature works as expected

- **lib**: Supporting libraries you have developed for your web application
- **tests**: Unit tests for testing your web application

  - **fixtures**: Fixtures created using factory_boy that are used to create
    model instances
  - **lib**: Unit tests which test libraries
  - **models**: Unit tests which test models
  - **views**: Unit tests which test views

- **bower.json**: Vendor provided client-side package requirements
- **config.py**: Configuration for development, production and test environments
- **manage.py**: Management interface and command registrations
- **setup.cfg**: General package configuration (used for nose)
- **requirements.txt**: Python package requirements

.. _Play: http://www.playframework.com/documentation/2.0/Anatomy
.. _Ruby on Rails: http://guides.rubyonrails.org/getting_started.html#creating-the-blog-application
.. _Flask-Migrate: https://github.com/miguelgrinberg/Flask-Migrate
.. _PyJade: https://github.com/SyrusAkbary/pyjade
.. _flask-failsafe: https://github.com/mgood/flask-failsafe
.. _nose: https://github.com/nose-devs/nose/
.. _Coverage.py: http://nedbatchelder.com/code/coverage
.. _factory_boy: https://github.com/rbarrois/factory_boy
.. _fake-factory: https://github.com/joke2k/faker
.. _behave: https://github.com/behave/behave
.. _splinter: http://splinter.cobrateam.info/
.. _selenium: https://code.google.com/p/selenium/
