# -*- coding: utf-8 -*-
import os
import sys
import codecs
import stat
from hashlib import md5
from fnmatch import fnmatch


PY3 = sys.version_info[0] == 3
if PY3:  # pragma: nocover
    def b(s):
        return s.encode("latin-1")
    raw_input = input
else:  # pragma: nocover
    def b(s):
        return s
    from __builtin__ import raw_input

def matches_any(filename, patterns):
    return any(fnmatch(filename, pattern) for pattern in patterns)


def get_permissions(filename):
    return stat.S_IMODE(os.stat(filename).st_mode)


def md5file(filename):
    return md5(codecs.open(filename).read()).hexdigest()


def md5data(data):
    return md5(b(data)).hexdigest()


def prompt_yes_no(question, default=None):
    choices = {
        'yes': True, 'ye': True, 'y': True,
        'no': False, 'n': False
    }

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
        answer = raw_input('%s [%s]: ' % (question, prompt)).lower()
        if answer in choices:
            return choices[answer]
        elif answer == '' and default:
            return choices[default]
        print('An invalid choice was entered, please enter y or n.')
