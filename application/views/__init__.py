# -*- coding: utf-8 -*-
"""
    flaskage.application.views
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Here you can create a number of files each containing a set of views
    which are grouped by Flask Blueprints.  Each set of views may be
    assigned a URL prefix so that they all appear under a particular URL.

    To access the global app object for retrieving config, you may use
    current_app.  For all other purposes, you should use the Blueprint mod
    object.

    Flask Quickstart Reference:
    http://flask.pocoo.org/docs/quickstart/

    SQLAlchemy ORM Tutorial:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html

    SQLAlchemy New Mexico Tech Quick Reference:
    http://infohost.nmt.edu/tcc/help/pubs/db/sqlalchemy/

    An example can be found below to get you started:

    from flask import Blueprint, render_template, current_app

    from .. import db
    from ..models.user import Model1, Model2, Model3

    mod = Blueprint('module1', __name__, url_prefix='/module1')


    @mod.route('/')
    def index():
        return render_template('index.html', data=data)

    Some basic SQLAlchemy queries are shown below:

    me = User(username='fgimian', name='Fotis')
    db.session.add(me)
    db.session.commit()
    my_id = me.id

    me = User.query.filter_by(username='oldusername').first()
    me.username = 'newusername'
    db.session.add(me)
    db.session.commit()

    me = User.query.filter_by(username='fgimian').first()
    db.session.delete(me)
    db.session.commit()

    users = User.query.all()

    :copyright: (c) 2014 Fotis Gimian.
    :license: Apache 2.0, see LICENSE for more details.
"""
