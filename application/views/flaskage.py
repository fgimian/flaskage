# -*- coding: utf-8 -*-
"""
    flaskage.application.views.flaskage
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    All views related to the Flaskage template application.

    :copyright: (c) 2014 Fotis Gimian.
    :license: MIT, see LICENSE for more details.
"""
from flask import Blueprint, render_template

mod = Blueprint('flaskage', __name__)


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/pyjade')
def index_pyjade():
    return render_template('index.jade')
