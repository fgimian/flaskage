# Flaskage #
*A complete and carefully designed template for use with the Flask web framework*

[![Build Status](https://travis-ci.org/fgimian/flaskage.png?branch=master)](https://travis-ci.org/fgimian/flaskage)

![Flaskage Logo](https://raw.github.com/fgimian/flaskage/master/application/static/img/flaskage.png)

Awesome artwork provided courtesy of [Open Clip Art Library](http://openclipart.org/detail/168585/knight-sheep-by-dodger2)

## About Flaskage ##

At the current time, [Flask](http://flask.pocoo.org/) is my favourite web framework in Python.  It's beautifully designed and every bit as powerful as the full-stack frameworks once you plug in the required components.

Unfortunately, there are currently only a few templates available to get you started with Flask.  All the existing templates are well worth checking out but didn't quite fit my needs and requirements, so I designed my own.

Some of the existing templates and projects which inspired and influenced this project are:

* [fbone](https://github.com/imwilsonxu/fbone)
* [overholt](https://github.com/mattupstate/overholt)
* [flask_website](https://github.com/mitsuhiko/flask/tree/website)
* [beancounter](https://bitbucket.org/audriusk/beancounter)
* [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask)

## Features ##

So what makes Flaskage unique?  A few little things:

* **Clean and simple**: Although I'm designing Flaskage for medium to larger sized projects, I wanted to ensure that the boilerplate code was kept to a minimum.  Instead, I've opted for comments which provide examples of what you can do rather than starting to write an application in the template.
* **One directory per function**: It seems that most templates are inspired by the way that Django separates apps, whereby each component of the larger web application has its own models, views, templates and static files.  I personally feel that this layout doesn't make sense.  Instead, I prefer a structure more similar to the [Play Framework](http://www.playframework.com/documentation/2.0/Anatomy) which keeps views in one directory, models in one directory and so on.  The ability to split views and models into multiple files is an absolute must which is also part of Flaskage's design.
* **Full integration of Flask-Assets**: This template has been designed for use with Coffeescript, LESS (in particular Twitter's Bootstrap CSS framework) or any other pre-processor you may have in mind.  Furthermore, Flaskage keeps all such uncompiled files neatly in an assets directory.
* **Database migrations**: Flaskage integrates [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) and is ready for database migrations which can be invoked via management commands.
* **Switchable configurations**: With a simple command line switch, you can run the development server under any environment you wish (development, production or testing).  Further to this, you can set a default environment for your app to run in via a variable in the config module or define your own custom config environments.
* **Flake8 integration**: You can check that your syntax is valid and that your coding style follows the PEP8 standard with a simple management command.
* **Clean client-side library integration**: Flaskage uses Bower and symlinks to cleanly integrate Twitter Bootstrap and jQuery with the ability to seamlessy upgrade these components when necessary and avoid duplication of the original source code in your Git repository.
* **Travis Integration**: Test case integration with Travis is provided out of the box.
* **Python 3 ready**: I have ported incompatible extensions (Flask-Bcrypt and Flask-Testing) to work across Python 2.6, 2.7 and 3.3 so that you're future-proof if and when you decide to move to a Python 3 environment.

## Project Structure ##

Flaskage is structured as shown below:

```
├── application       : Main web application directory with app initialisation
│   ├── assets        : Pre-compiled script and stylsheet assets
│   ├── models        : Database model definitions
│   ├── static        : Static files such as CSS, Javascript and images
│   ├── templates     : Jinja2 templates for presentation
│   ├── vendor        : Vendor provided script and stylesheet assets
│   └── views         : Views and related forms that provide business logic for each page
├── libraries         : Supporting libraries you have developed for your web application
├── tests             : Unit tests for testing your web application
├── bower.json        : Vendor provided client-side package requirements
├── config.py         : Configuration for development, production and test environments
├── manage.py         : Management interface and command registrations
└── requirements.txt  : Python package requirements
```

## Preparing Your Python Environment ##

Flaskage supports the following Python versions:

* CPython 2.6
* CPython 2.7
* CPython 3.3
* PyPy 2.2

Create a virtualenv and install the required Python packages:

``` bash
mkdir ~/.virtualenv
virtualenv ~/.virtualenv/flaskage
source ~/.virtualenv/flaskage/bin/activate
pip install -r requirements.txt
```

If you're on Python 2.6, you'll also need to install some extra packages:

``` bash
pip install -r requirements-2.6.txt
```

## Installing Node.js Components ##

In order to use Bower, LESS, Clean CSS, Coffeescript and UglifyJS, we need to install the necessary modules on our system via Node.js.

Firstly, ensure that your system has the latest [Node.js](http://nodejs.org/) installed and then run the following:

``` bash
sudo npm install -g bower less clean-css coffee-script uglify-js
```

## Installing jQuery and Twitter Bootstrap with Bower ##

From the project root directory, install the client-side libraries as follows:

``` bash
bower install
```

## Using the Template ##

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
./manage.py tests
```

You may validate all your code using Flaka8 like this:

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

In addition, you may consider plugging in a client-side Javascript framework for a more dynamic page.  Some popular examples of these are:

* [AngularJS](http://angularjs.org/)
* [Backbone.js](http://backbonejs.org/)
* [Ember.js](http://emberjs.com/)
* [knockout](http://knockoutjs.com/)
