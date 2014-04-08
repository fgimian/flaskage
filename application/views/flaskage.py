# -*- coding: utf-8 -*-
from flask import Blueprint, render_template

mod = Blueprint('flaskage', __name__)


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/pyjade')
def index_pyjade():
    return render_template('index.jade')
