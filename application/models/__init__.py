# -*- coding: utf-8 -*-
from .. import db


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

# Import models from the various model files
# from .<submodule> import <model>  # noqa
