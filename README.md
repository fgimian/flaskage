# Flaskage #
*A complete and carefully designed template for use with the Flask web framework*

[![Build Status](https://travis-ci.org/fgimian/flaskage.png?branch=master)](https://travis-ci.org/fgimian/flaskage)

![Flaskage Logo](https://raw.github.com/fgimian/flaskage/master/application/static/img/flaskage.png)

Awesome artwork provided courtesy of [Open Clip Art Library](http://openclipart.org/detail/168585/knight-sheep-by-dodger2)

## Documentation ##

Please check out the [Flaskage documentation at Read the Docs](http://flaskage.readthedocs.org/).

## Using Flaskage ##

From the project root directory, you may now run your server as follows:

``` bash
./manage.py runserver -t 0.0.0.0
```

You may optionally run the server in a chosen configuration environment:

``` bash
./manage.py runserver -t 0.0.0.0 -c production
```

All unit tests may be run using:

``` bash
./manage.py test
```

You may validate all your code using Flake8 like this:

``` bash
./manage.py flake8
```

Furthermore, you have access to management commands that list URLs and their view functions, start a shell, manage assets, perform database migrations and clean up \*.pyc and \*.pyo files.  Simply run the **./manage.py** script to see further details.

## Suggested Additional Libraries ##

Depending on the circumstances, you may wish to integrate the following additional Flask libraries into your application:

* [Flask-Babel](http://pythonhosted.org/Flask-Babel/): Internationalisation support
* [Flask-Cache](http://pythonhosted.org/Flask-Cache/): Caching for chosen items in your application
* [Flask-Mail](http://pythonhosted.org/Flask-Mail/): When your application needs to send emails to users
* [Flask-Principal](http://pythonhosted.org/Flask-Principal/): For more fine-tuned granularity of user account types and permissions
* [Flask-Testing](https://pythonhosted.org/Flask-Testing/): For a few handy test helpers which make testing certain aspects simpler

In addition, you may consider plugging in a client-side Javascript framework for a more dynamic page.  Some popular examples of these are:

* [AngularJS](http://angularjs.org/)
* [Backbone.js](http://backbonejs.org/)
* [Ember.js](http://emberjs.com/)
* [knockout](http://knockoutjs.com/)

## Future Plans for Flaskage ##

* **Skeleton Integration**: Flaskage will soon be converted into a [mr.bob](https://github.com/iElectric/mr.bob) or [cookiecutter](https://github.com/audreyr/cookiecutter) template so that new projects may easily be generated.
* **Deployment Solutions**: I hope to add example configuration files and scripts which demonstrate how Flaskage may be deployed on a production web server.
* **Further Documentation**: I intend to start a Wiki for this project to provide examples of common tasks along with tips and tricks.
