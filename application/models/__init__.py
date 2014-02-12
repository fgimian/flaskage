# -*- coding: utf-8 -*-
"""
    flaskage.application.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Here you can create a number of files each containing model definitions
    via the SQLAlchemy ORM.

    SQLAlchemy ORM Reference:
    http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/declarative.html

    A detailed example can be found below to get you started:

    from datetime import datetime

    from flask.ext.login import UserMixin

    from .. import db, bcrypt


    MALE = 1
    FEMALE = 2
    OTHER = 3
    SEX_TYPE = {
        MALE: 'Male',
        FEMALE: 'Female',
        OTHER: 'Other',
    }


    class User(db.Model, UserMixin):
        # Optionally override the table name (default is user anyway)
        __tablename__ = 'user'

        id = db.Column('id', db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=False, unique=True)
        email = db.Column(db.String(100), unique=True)
        _password = db.Column('password', db.String(120), nullable=False)
        sex_code = db.Column(db.Integer)
        creation_date = db.Column(db.DateTime, default=datetime.utcnow)

        # Column with custom name
        active = db.Column('is_active', db.Boolean, default=False)

        def _get_password(self):
            return self._password

        def _set_password(self, password):
            self._password = bcrypt.generate_password_hash(password)

        password = db.synonym(
            '_password', descriptor=property(_get_password, _set_password))

        def check_password(self, password):
            if self.password is None:
                return False
            return bcrypt.check_password_hash(self.password, password)

        @property
        def sex(self):
            return SEX_TYPE.get(self.sex_code)

        def __eq__(self, other):
            return (self.username == other or
                    self.username == getattr(other, 'username', None))

        def __ne__(self, other):
            return (self.username != other and
                    self.username != getattr(other, 'username', None))

        def __repr__(self):
            return "User <%r>" % self.username


    class Category(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return '<Category %r>' % self.name


    # Many to many relationship table definition
    users_posts = db.Table(
        'users_posts',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('post_id', db.Integer(), db.ForeignKey('post.id')))


    class Post(db.Model):

        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(80))
        body = db.Column(db.Text)
        pub_date = db.Column(db.DateTime, default=datetime.utcnow)
        number_of_edits = db.Column(db.Numeric)

        # One to many relationship (note that you may also place tho
        # relationship line in the Category class in reverse if you like)
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        category = db.relationship('Category', backref=db.backref('posts'))

        # Many to many relationship
        users = db.relationship('User', secondary=users_posts,
                                backref=db.backref('posts'))

        def __init__(self, title, body, category):
            self.title = title
            self.body = body
            self.category = category

        def __repr__(self):
            return '<Post %r>' % self.title

    :copyright: (c) 2014 Fotis Gimian.
    :license: Apache 2.0, see LICENSE for more details.
"""
