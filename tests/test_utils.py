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
    matches_any, get_permissions, md5_file, md5_data, prompt_yes_no
)


class TestUtils:

    def test_matches_any_match(self):
        assert matches_any('hello.txt', ['abc.txt', '*.txt'])

    def test_matches_any_no_match(self):
        assert not matches_any('hello.txt', ['abc.txt' '*.py'])

    def test_get_permissions(self):
        f = NamedTemporaryFile(delete=False)
        f.close()
        os.chmod(
            f.name,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
            stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH
        )
        assert get_permissions(f.name) == 0o754
        os.unlink(f.name)

    def test_md5_file(self):
        f = NamedTemporaryFile(delete=False)
        f.write(b'hello there')
        f.close()
        md5sum = md5_file(f.name)
        os.unlink(f.name)
        assert md5sum == '161bc25962da8fed6d2f59922fb642aa'

    def test_md5_data(self):
        assert md5_data('hello there') == '161bc25962da8fed6d2f59922fb642aa'

    @mock.patch('flaskage.utils.input', return_value='')
    def test_prompt_yes_no_default_yes(self, mock_raw_input):
        assert prompt_yes_no('Shall I go ahead?', default='y')

    @mock.patch('flaskage.utils.input', return_value='')
    def test_prompt_yes_no_default_no(self, mock_raw_input):
        assert not prompt_yes_no('Shall I go ahead?', default='n')

    @mock.patch('flaskage.utils.input', return_value='y')
    def test_prompt_yes_no_reply_yes(self, mock_raw_input):
        assert prompt_yes_no('Shall I go ahead?')

    @mock.patch('flaskage.utils.input', return_value='n')
    def test_prompt_yes_no_reply_no(self, mock_raw_input):
        assert not prompt_yes_no('Shall I go ahead?', default='y')

    @mock.patch('flaskage.utils.input', side_effect=['bla', 'n'])
    def test_prompt_yes_no_reply_invalid(self, mock_raw_input):
        with mock.patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            assert not prompt_yes_no('Shall I go ahead?')
        assert 'An invalid choice was entered' in mock_stdout.getvalue()

    @raises(ValueError)
    def test_prompt_yes_no_invalid_default(self):
        prompt_yes_no('Shall I go ahead?', default='bla')
