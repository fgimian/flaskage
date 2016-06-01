# Flaskage

[![Build Status](https://travis-ci.org/fgimian/flaskage.png?branch=master)](https://travis-ci.org/fgimian/flaskage)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/fgimian/flaskage/blob/master/LICENSE)

**Please note that this project is a work in progress**

![Flaskage Logo](https://raw.githubusercontent.com/fgimian/flaskage/master/images/flaskage-logo.png)

Awesome artwork provided courtesy of
[Open Clip Art Library](http://openclipart.org/detail/168585/knight-sheep-by-dodger2)

## Introduction

The Flaskage template attempts to bring together all the best packages and
integrate them with Flask so you have a full stack MVC (or MTV) structure
ready-to-use.

Flaskage takes a lot of inspiration from frameworks like Ruby on Rails, Play
and Laravel and doesn’t attempt to re-create the Django way of working.

## Quick Start

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

## Documentation

Please check out the [Flaskage documentation at Read the Docs](http://flaskage.readthedocs.org/).

## License

Flaskage is released under the **MIT** license. Please see the
[LICENSE](https://github.com/fgimian/flaskage/blob/master/LICENSE)
file for more details.

## TODO

### CLI

* Complete unit tests for the flaskage CLI tool
* Consider a scaffolding command for BDD and Jade templates

### Project Structure

* Determine the best way to deal with symbolic link for Twitter Bootstrap fonts

### Documentation

* Complete writing documentation

### Long-term goals are as follows

* Generation of scaffolding including CRUD
* Pluggable scaffolding modules
* Ability to generate foreign keys and relationships via scaffolding
* Consider supporting a Django-like directory layout
