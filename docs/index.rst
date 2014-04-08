Welcome to Flaskage
===================

Welcome to Flaskage's documentation.  The Flaskage template attempts to bring
together all the best packages and integrate them into Flask so you have a 
ull stack MVC structure ready-to-use.

Flaskage takes a lot of inspiration from frameworks like
`Ruby on Rails <http://rubyonrails.org/>`_,
`Play <http://www.playframework.com/>`_ and `Laravel <http://laravel.com/>`_
and doesn't attempt to re-create the Django way of working.

In addition to providing a template, this project also intends to document
common workflows with the template and serve as a good starting point of
reference.

Some of the existing templates and projects which inspired and influenced this
project are:

- `overholt <https://github.com/mattupstate/overholt>`_
- `flasky <https://github.com/miguelgrinberg/flasky>`_
- `flask_website <https://github.com/mitsuhiko/flask/tree/website>`_
- `beancounter <https://bitbucket.org/audriusk/beancounter>`_
- `flaskr-bdd <https://github.com/ismaild/flaskr-bdd>`_
- `fbone <https://github.com/imwilsonxu/fbone>`_
- `cookiecutter-flask <https://github.com/sloria/cookiecutter-flask>`_
- `flask-chassis <https://github.com/SawdustSoftware/flask-chassis>`_

User's Guide
------------

This part of the documentation focuses on using Flaskage along with common
patterns that you can use as a reference while developing your application.

.. toctree::
   :maxdepth: 2

   overview
   installation
   configuring
   database_design
   database_queries
   unit_testing_models
   blueprints
   client_side_libraries
   asset_pipeline
   jinja2_templates
   pyjade_templates
   unit_testing_views
   bdd_testing
