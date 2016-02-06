# Flaskage #
*A complete and carefully designed template for use with the Flask web framework*

[![Build Status](https://travis-ci.org/fgimian/flaskage.png?branch=master)](https://travis-ci.org/fgimian/flaskage)

![Flaskage Logo](https://raw.githubusercontent.com/fgimian/flaskage/master/docs/_static/flaskage-full.png)

Awesome artwork provided courtesy of [Open Clip Art Library](http://openclipart.org/detail/168585/knight-sheep-by-dodger2)

## Documentation ##

Please check out the [Flaskage documentation at Read the Docs](http://flaskage.readthedocs.org/).

## Quick Start ##

Install Flaskage in your virtualenv as follows:

``` bash
pip install git+git://github.com/fgimian/flaskage.git
```

Create a new project:

``` bash
flaskage new <project-name>
```

Start the development server and check out your new project:

``` bash
cd <project-name>
./manage.py server
```

Refer to the [documentation](http://flaskage.readthedocs.org/) for further instruction.

## TODO ##

Flaskage is currently a work in progress.  My current outstanding tasks are...

CLI:

* Complete unit tests for the flaskage CLI tool
* Consider a scaffolding command for BDD and Jade templates

Project Structure:

* Determine the best way to deal with symbolic link for Twitter Bootstrap fonts

Documentation:

* Complete writing documentation

Long-term goals are as follows:

* Generation of scaffolding including CRUD
* Pluggable scaffolding modules
* Ability to generate foreign keys and relationships via scaffolding
* Consider supporting a Django-like directory layout
