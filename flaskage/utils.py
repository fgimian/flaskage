# -*- coding: utf-8 -*-
import os
import re
import sys
import codecs
import stat
from hashlib import md5
from fnmatch import fnmatch

import click

PY3 = sys.version_info[0] == 3
if PY3:  # pragma: nocover
    def b(s):
        return s.encode("latin-1")
else:  # pragma: nocover
    def b(s):
        return s
    from __builtin__ import raw_input as input


def matches_any(filename, patterns):
    return any(fnmatch(filename, pattern) for pattern in patterns)


def get_permissions(filename):
    return stat.S_IMODE(os.stat(filename).st_mode)


def md5_file(filename):
    with codecs.open(filename) as f:
        data = f.read()
    return md5(data).hexdigest()


def md5_data(data):
    return md5(b(data)).hexdigest()


def prompt_yes_no(question, default=None):
    choices = {'yes': True, 'y': True, 'no': False, 'n': False}

    if default is None:
        prompt = 'y/n'
    elif default.lower() in choices:
        if choices[default]:
            prompt = 'Y/n'
        else:
            prompt = 'y/N'
    else:
        raise ValueError('Invalid default value specified')

    while True:
        answer = input('%s [%s]: ' % (question, prompt)).lower().strip()
        if answer in choices:
            return choices[answer]
        elif answer == '' and default:
            return choices[default]
        print('An invalid choice was entered, please enter y or n.')


def camelcase(s):
    return ''.join([i.title() or '_' for i in s.split('_')])


def valid_underscore_name(s):
    return re.match(r'^[a-z_][a-z0-9_]*$', s)


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


class ModuleNameParamType(click.ParamType):
    name = 'module_name'

    def convert(self, value, param, ctx):
        if valid_underscore_name(value):
            return value
        else:
            self.fail('%s is not a valid module name' % value, param, ctx)

    def __repr__(self):
        return 'MODULE_NAME'

MODULE_NAME = ModuleNameParamType()
