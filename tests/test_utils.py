# -*- coding: utf-8 -*-
import os
import stat
from tempfile import NamedTemporaryFile
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import mock
from nose.tools import raises

from flaskage.utils import (
    matches_any, get_permissions, md5_file, md5_data, prompt_yes_no,
    camelcase, valid_underscore_name
)


def test_matches_any_match():
    assert matches_any('hello.txt', ['abc.txt', '*.txt'])


def test_matches_any_no_match():
    assert not matches_any('hello.txt', ['abc.txt' '*.py'])


def test_get_permissions():
    f = NamedTemporaryFile(delete=False)
    f.close()
    os.chmod(
        f.name,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH
    )
    assert get_permissions(f.name) == 0o754
    os.unlink(f.name)


def test_md5_file():
    f = NamedTemporaryFile(delete=False)
    f.write(b'hello there')
    f.close()
    md5sum = md5_file(f.name)
    os.unlink(f.name)
    assert md5sum == '161bc25962da8fed6d2f59922fb642aa'


def test_md5_data():
    assert md5_data('hello there') == '161bc25962da8fed6d2f59922fb642aa'


@mock.patch('flaskage.utils.input', return_value='')
def test_prompt_yes_no_default_yes(mock_raw_input):
    assert prompt_yes_no('Shall I go ahead?', default='y')


@mock.patch('flaskage.utils.input', return_value='')
def test_prompt_yes_no_default_no(mock_raw_input):
    assert not prompt_yes_no('Shall I go ahead?', default='n')


@mock.patch('flaskage.utils.input', return_value='y')
def test_prompt_yes_no_reply_yes(mock_raw_input):
    assert prompt_yes_no('Shall I go ahead?')


@mock.patch('flaskage.utils.input', return_value='n')
def test_prompt_yes_no_reply_no(mock_raw_input):
    assert not prompt_yes_no('Shall I go ahead?', default='y')


@mock.patch('flaskage.utils.input', side_effect=['bla', 'n'])
def test_prompt_yes_no_reply_invalid(mock_raw_input):
    with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        assert not prompt_yes_no('Shall I go ahead?')
    assert 'An invalid choice was entered' in mock_stdout.getvalue()


@raises(ValueError)
def test_prompt_yes_no_invalid_default():
    prompt_yes_no('Shall I go ahead?', default='bla')


def test_camelcase():
    assert camelcase('hello_there_mate') == 'HelloThereMate'


def test_camelcase_leading_underscore():
    assert camelcase('_leading_underscore') == '_LeadingUnderscore'


def test_valid_underscore_name_valid():
    assert valid_underscore_name('hello_there_mate')


def test_valid_underscore_name_invalid():
    assert not valid_underscore_name('HelloThereMate')


def test_valid_underscore_name_invalid_starting_with_number():
    assert not valid_underscore_name('1module_name')
