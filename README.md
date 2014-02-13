# Flaskage #
*A complete and carefully designed template for use with the Flask web framework*

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
* **Switchable configurations**: With a simple command line switch, you can run the development server under any environment you wish (development, production or testing).  Further to this, you can set a default environment for your app to run in via a variable in the config module.
* **Flake8 integration**: You can check that your syntax is valid and that your coding style follows the PEP8 standard with a simple management command.

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

## Adding Node.js Compilers and Minifiers ##

In order to use LESS, Clean CSS, Coffeescript and UglifyJS, we need to install the necessary modules on our system via Node.js.

Firstly, ensure that your system has the latest [Node.js and NPM](http://nodejs.org/) installed and then run the following:

``` bash
sudo npm install -g bower less clean-css coffee-script uglify-js
```

## Adding jQuery and Twitter Bootstrap ##

Please ensure you start in the **flaskage** directory:

``` bash
cd flaskage/
```

And now install all the client-side libraries using bower:

``` bash
bower install
```

## Using the Template ##

Ensure that you are in the **flaskage** directory:

``` bash
cd flaskage/
```

You may now run your server as follows:

``` bash
./manage.py runserver -t 0.0.0.0
```

All unit tests may be run using:

``` bash
./manage.py test
```

You may validate all your code using Flaka8 like this:

``` bash
./manage.py flake8
```

Furthermore, you have access to management commands that list URLs and their view functions, start a shell, manage assets, perform database migrations and clean up \*.pyc and \*.pyo files.  Simply run the **./manage.py** script to see further details.

## Remaining Tasks ##

This project is a work in progress and will be improved over time as I begin to use it further for building web applications.  The remaining tasks on my list at present are as follows:

* Determine if Flask-Login is worth integrating as an auth system
