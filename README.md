# Flaskage #
*A complete and carefully designed template for use with the Flask web framework*

[![Build Status](https://travis-ci.org/fgimian/flaskage.png?branch=master)](https://travis-ci.org/fgimian/flaskage)

![Flaskage Logo](https://raw.github.com/fgimian/flaskage/master/application/static/img/flaskage.png)

Awesome artwork provided courtesy of [Open Clip Art Library](http://openclipart.org/detail/168585/knight-sheep-by-dodger2)

## About Flaskage ##

At the current time, [Flask](http://flask.pocoo.org/) is my favourite web framework in Python.  It's beautifully designed and every bit as powerful as the full-stack frameworks once you plug in the required components.

Unfortunately, there are currently only a few templates available to get you started with Flask.  All the existing templates are well worth checking out but didn't quite fit my needs and requirements, so I designed my own.

Some of the existing templates and projects which inspired and influenced this project are:

* [overholt](https://github.com/mattupstate/overholt)
* [flasky](https://github.com/miguelgrinberg/flasky)
* [flask_website](https://github.com/mitsuhiko/flask/tree/website)
* [beancounter](https://bitbucket.org/audriusk/beancounter)
* [fbone](https://github.com/imwilsonxu/fbone)
* [cookiecutter-flask](https://github.com/sloria/cookiecutter-flask)
* [flask-chassis](https://github.com/SawdustSoftware/flask-chassis)

## Features ##

So what makes Flaskage unique?  A few little things:

* **Clean and simple**: Although I'm designing Flaskage for medium to larger sized projects, I wanted to ensure that the boilerplate code was kept to a minimum.  Instead, I've opted for comments which provide examples of what you can do rather than starting to write an application in the template.
* **One directory per function**: It seems that most templates are inspired by the way that Django separates apps, whereby each component of the larger web application has its own models, views, templates and static files.  I personally feel that this layout doesn't make sense.  Instead, I prefer a structure more similar to the [Play Framework](http://www.playframework.com/documentation/2.0/Anatomy) or [Ruby on Rails](http://guides.rubyonrails.org/getting_started.html#creating-the-blog-application) which keeps views in one directory, models in one directory and so on.  The ability to split views and models into multiple files is an absolute must which is also part of Flaskage's design.
* **Full integration of Flask-Assets**: This template has been designed for use with Coffeescript, LESS (in particular Twitter's Bootstrap CSS framework) or any other pre-processor you may have in mind.  Furthermore, Flaskage keeps all such uncompiled files neatly in an assets directory.
* **Database migrations**: Flaskage integrates [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) and is ready for database migrations which can be invoked via management commands.
* **PyJade integration**: If you choose to, you can may use [PyJade](https://github.com/SyrusAkbary/pyjade) to write your templates.  This is a far less verbose language than regular HTML.
* **Switchable configurations**: With a simple command line switch, you can run the development server under any environment you wish (development, production or testing).  Further to this, you can set a default environment for your app to run in via a variable in the config module or define your own custom config environments.
* **Flake8 integration**: You can check that your syntax is valid and that your coding style follows the PEP8 standard with a simple management command.
* **Clean client-side library integration**: Flaskage uses Bower and symlinks to cleanly integrate Twitter Bootstrap and jQuery with the ability to seamlessly upgrade these components when necessary and avoid duplication of the original source code in your Git repository.
* **More robust development server**: Using my own fork of [flask-failsafe](https://github.com/mgood/flask-failsafe), the development server won't crash each time small errors are made while coding.
* **Travis Integration**: Test case integration with Travis is provided out of the box.
* **Powerful test tools**: Integrated use of [nose](https://github.com/nose-devs/nose/), [Coverage.py](http://nedbatchelder.com/code/coverage), [factory_boy](https://github.com/rbarrois/factory_boy) and [fake-factory](https://github.com/joke2k/faker).
* **Python 3 ready**: I have only chosen extensions which work across Python 2.6, 2.7 and 3.3 so that you're future-proof if and when you decide to move to a Python 3 environment.

## Project Structure ##

Flaskage is structured as shown below:

```
├── application           : Main web application directory with app initialisation
│   ├── assets            : Pre-compiled script and stylsheet assets
│   ├── models            : Database model definitions
│   ├── static            : Static files such as CSS, Javascript and images
│   ├── templates         : Jinja2 templates for presentation
│   ├── vendor            : Vendor provided script and stylesheet assets
│   └── views             : Views and related forms that provide business logic for each page
├── libraries             : Supporting libraries you have developed for your web application
├── tests                 : Unit tests for testing your web application
│   ├── fixtures          : Fixtures created using factory_boy that are used to create model instances
│   ├── models            : Unit tests which test models
│   └── views             : Unit tests which test views
├── bower.json            : Vendor provided client-side package requirements
├── config.py             : Configuration for development, production and test environments
├── manage.py             : Management interface and command registrations
└── requirements.txt      : Python package requirements
```

## Preparing Your Operating System ##

Flaskage supports the following Linux operating systems:

* Debian 6 (Squeeze)
* Debian 7 (Wheezy)
* Ubuntu Server 10.04 LTS (Lucid Lynx)
* Ubuntu Server 12.04 LTS (Precise Pangolin)
* CentOS 5.x
* CentOS 6.x
* Red Hat Enterprise Linux 5.x
* Red Hat Enterprise Linux 6.x

You'll need to install some pre-requisites to ensure that all Python packages install correctly.

If you're running Python 3.3 on Ubuntu Server 12.04:

``` bash
sudo apt-get install gcc python3.3-dev
```

If you're running Python 2.6 or 2.7 Debian or Ubuntu Server:

``` bash
sudo apt-get install gcc python-dev
```

If you're running CentOS 6.x or Red Hat Enterprise Linux 6.x:

``` bash
sudo yum install gcc python-devel
```

If you're running CentOS 5.x or Red Hat Enterprise Linux 5.x, you'll need to use the **python26** package from [EPEL](https://fedoraproject.org/wiki/EPEL).  You may then install required dependencies as follows:

``` bash
sudo yum install gcc python26-devel
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

## Installing Node.js Components ##

In order to use Bower, LESS, Clean CSS, Coffeescript and UglifyJS, we need to install the necessary modules on our system via Node.js.

Firstly, ensure that your system has the latest [Node.js](http://nodejs.org/) installed and then run the following:

``` bash
[sudo] npm install -g bower less clean-css coffee-script uglify-js
```

If your Node.js installation is global and owned by root, you'll need to run the command above using sudo.

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
./manage.py test
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
