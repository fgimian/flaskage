# -*- coding: utf-8 -*-
from shutil import rmtree
from tempfile import mkdtemp
import os
import stat
import logging

import jinja2
from jinja2 import Environment, StrictUndefined
import mock
from nose.tools import raises

import flaskage
from flaskage.scaffold import Scaffold, ScaffoldException
from flaskage.utils import get_permissions


class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [], 'info': [], 'warning': [], 'error': [], 'critical': []
        }


class TestScaffold:
    @classmethod
    def setup_class(cls):
        # Create a mock handler instance at the highest logging level
        cls.mock_log_handler = MockLoggingHandler(level=logging.DEBUG)

        # Grab the main logger at the highest logging level
        cls.logger = logging.getLogger('flaskage.scaffold')
        cls.logger.setLevel(logging.DEBUG)

        # Disable logging to the console for our main logger
        cls.logger.propagate = False

        # Add the mock handler to our main logger
        cls.logger.addHandler(cls.mock_log_handler)

    @classmethod
    def teardown_class(cls):
        # Remove the mock handler from the logger
        cls.logger.removeHandler(cls.mock_log_handler)

    def setup(self):
        self.temp_dir = mkdtemp()
        self.build_dir = os.path.join(self.temp_dir, 'test')
        self.templates = os.path.abspath(
            os.path.join(
                os.path.dirname(flaskage.__file__), os.pardir, 'tests',
                'templates'
            )
        )
        self.mock_log_handler.reset()

    def teardown(self):
        rmtree(self.temp_dir)

    def build_scaffold(self, template_dir, **kwargs):
        scaffold = Scaffold(
            os.path.join(self.templates, template_dir), self.build_dir,
            **kwargs
        )
        scaffold.render_structure()

    def exists(self, filename, type='file'):
        file_path = os.path.join(self.build_dir, filename)
        if type == 'file':
            return os.path.isfile(file_path)
        elif type == 'dir':
            return os.path.isdir(file_path)
        elif type == 'link':
            return os.path.islink(file_path)
        else:
            raise Exception('invalid type specified')

    def contents(self, filename):
        file_path = os.path.join(self.build_dir, filename)
        return open(file_path).read()

    def logged(self, search_text, level='info'):
        return any(
            [m for m in self.mock_log_handler.messages[level]
             if search_text in m]
        )

    # ------------------------------------------------------------------------
    # Test Customisations in Constructor
    # ------------------------------------------------------------------------
    def test_variables_valid(self):
        self.build_scaffold(
            'test-template-3', variables={'name': 'Pumpkinhead'}
        )
        assert self.exists('filea')
        assert self.exists('fileb.html')
        assert 'Pumpkinhead' in self.contents('filea')
        assert '{{{ name }}}' in self.contents('fileb.html')

    @raises(jinja2.exceptions.UndefinedError)
    def test_variables_missing_template(self):
        self.build_scaffold(
            'test-template-3', variables={'author': 'Pumpkinhead'}
        )

    @raises(ScaffoldException)
    def test_variables_missing_filename(self):
        self.build_scaffold(
            'test-template-5', variables={'author': 'Pumpkinhead'}
        )

    @raises(ScaffoldException)
    def test_overwrite_root_disallowed(self):
        os.mkdir(self.build_dir)
        self.build_scaffold('test-template-1')

    def test_overwrite_root_allowed(self):
        os.mkdir(self.build_dir)
        self.build_scaffold('test-template-1', overwrite_target_root=True)
        assert self.exists('directorya', type='dir')
        assert self.exists('directoryb', type='dir')
        assert self.exists('directoryc', type='dir')
        assert self.exists('direxclude123', type='dir')
        assert self.exists('exclude1', type='dir')
        assert self.exists('exclude2', type='dir')
        assert self.exists('filea.txt', type='file')
        assert self.exists('fileb.py', type='file')
        assert self.exists('filec.md', type='file')
        assert self.exists('filed.py', type='file')

    def test_ignored_files(self):
        self.build_scaffold(
            'test-template-1', ignored_files=['*.txt', 'filec.md']
        )
        assert self.exists('directorya', type='dir')
        assert self.exists('directoryb', type='dir')
        assert self.exists('directoryc', type='dir')
        assert self.exists('direxclude123', type='dir')
        assert self.exists('exclude1', type='dir')
        assert self.exists('exclude2', type='dir')
        assert not self.exists('filea.txt', type='file')
        assert self.exists('fileb.py', type='file')
        assert not self.exists('filec.md', type='file')
        assert self.exists('filed.py', type='file')

    def test_ignored_dirs(self):
        self.build_scaffold(
            'test-template-1', ignored_dirs=['*exclude*', 'directorya']
        )
        assert not self.exists('directorya', type='dir')
        assert self.exists('directoryb', type='dir')
        assert self.exists('directoryc', type='dir')
        assert not self.exists('direxclude123', type='dir')
        assert not self.exists('exclude1', type='dir')
        assert not self.exists('exclude2', type='dir')
        assert self.exists('filea.txt', type='file')
        assert self.exists('fileb.py', type='file')
        assert self.exists('filec.md', type='file')
        assert self.exists('filed.py', type='file')

    def test_template_extension(self):
        self.build_scaffold(
            'test-template-3', template_extension='.html',
            variables={'name': 'Pumpkinhead'}
        )
        assert self.exists('filea.jinja')
        assert self.exists('fileb')
        assert '{{{ name }}}' in self.contents('filea.jinja')
        assert 'Pumpkinhead' in self.contents('fileb')

    def test_template_extension_no_dot(self):
        self.build_scaffold(
            'test-template-3', template_extension='html',
            variables={'name': 'Pumpkinhead'}
        )
        assert self.exists('filea.jinja')
        assert self.exists('fileb')
        assert '{{{ name }}}' in self.contents('filea.jinja')
        assert 'Pumpkinhead' in self.contents('fileb')

    def test_template_extension_everything_is_template(self):
        self.build_scaffold(
            'test-template-3', template_extension=None,
            variables={'name': 'Pumpkinhead'}
        )
        assert self.exists('filea.jinja')
        assert self.exists('fileb.html')
        assert 'Pumpkinhead' in self.contents('filea.jinja')
        assert 'Pumpkinhead' in self.contents('fileb.html')

    def test_jinja2_env(self):
        self.build_scaffold(
            'test-template-4', variables={'name': 'Pumpkinman'},
            jinja2_env=Environment(
                block_start_string='{{%=', block_end_string='=%}}',
                variable_start_string='{{=', variable_end_string='=}}',
                trim_blocks=True, undefined=StrictUndefined
            )
        )
        assert self.exists('filea')
        assert self.exists('fileb.html')
        assert 'My name is Pumpkinman' in self.contents('filea')
        assert (
            "{{%= if name == 'Pumpkinman' =%}}" in self.contents('fileb.html')
        )
        assert ' My name is {{= name =}}' in self.contents('fileb.html')

    # ------------------------------------------------------------------------
    # Test Files & Templates
    # ------------------------------------------------------------------------
    def test_files_and_templates(self):
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('happyman', type='file')
        assert 'happyman is 25 years old' in self.contents('happyman')
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert self.exists('fileb', type='file')
        assert 'I am 25 years old' in self.contents('fileb')
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')

    def test_policy_skip_file_content(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Some random text' in self.contents('filec.txt')
        assert self.logged('Skipping existing file')

    def test_policy_skip_file_permissions(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Hello there {{{ name }}}\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_file_content(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Some random text' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_file_content(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Copying and overwriting file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_file_permissions(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Hello there {{{ name }}}\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_file_permissions(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Hello there {{{ name }}}\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Updating permissions of file')

    def test_policy_overwrite_file_content(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Copying and overwriting file')

    def test_policy_overwrite_file_permissions(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Hello there {{{ name }}}\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt', type='file')
        assert 'Hello there {{{ name }}}' in self.contents('filec.txt')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Updating permissions of file')

    def test_skip_identical_file(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filec.txt')
        with open(test_file, 'w') as f:
            f.write('Hello there {{{ name }}}\n')
        os.chmod(
            test_file,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP |
            stat.S_IROTH
        )
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filec.txt')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Skipping identical file')

    def test_policy_skip_template_content(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'Some random text' in self.contents('filea')
        assert self.logged('Skipping existing file')

    def test_policy_skip_template_permissions(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('My name is happyman\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_template_content(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'Some random text' in self.contents('filea')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_template_content(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Rendering and overwriting template')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_template_permissions(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('My name is happyman\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o600
        assert self.logged('Skipping existing file')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_template_permissions(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('My name is happyman\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Updating permissions of template')

    def test_policy_overwrite_template_content(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('Some random text')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Rendering and overwriting template')

    def test_policy_overwrite_template_permissions(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('My name is happyman\n')
        os.chmod(test_file, stat.S_IRUSR | stat.S_IWUSR)
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea', type='file')
        assert 'My name is happyman' in self.contents('filea')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Updating permissions of template')

    def test_skip_identical_template(self):
        os.mkdir(self.build_dir)
        test_file = os.path.join(self.build_dir, 'filea')
        with open(test_file, 'w') as f:
            f.write('My name is happyman\n')
        os.chmod(
            test_file,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP |
            stat.S_IROTH
        )
        self.build_scaffold(
            'test-template-6', overwrite_target_root=True,
            variables={'name': 'happyman', 'age': 25}
        )
        assert self.exists('filea')
        assert get_permissions(test_file) == 0o664
        assert self.logged('Skipping identical file')

    def test_skip_non_file(self):
        os.mkdir(self.build_dir)
        replace_file = os.path.join(self.build_dir, 'filea.txt')
        os.mkdir(replace_file)
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('filea.txt', type='dir')
        assert self.logged('Skipping existing non-file', level='error')

    # ------------------------------------------------------------------------
    # Test Directories
    # ------------------------------------------------------------------------
    def test_directory(self):
        self.build_scaffold(
            'test-template-5', overwrite_target_root=True,
            variables={'name': 'happyman'}
        )
        assert self.exists('happyman', type='dir')
        assert self.exists('directory1', type='dir')
        assert self.exists('directory2', type='dir')

    def test_policy_skip_directory(self):
        os.mkdir(self.build_dir)
        test_directory = os.path.join(self.build_dir, 'directory1')
        os.mkdir(test_directory)
        os.chmod(test_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP
        )
        assert self.exists('directory1', type='dir')
        assert get_permissions(test_directory) == 0o700
        assert self.logged('Skipping existing directory')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_directory(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_directory = os.path.join(self.build_dir, 'directory1')
        os.mkdir(test_directory)
        os.chmod(test_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT
        )
        assert self.exists('directory1', type='dir')
        assert get_permissions(test_directory) == 0o700
        assert self.logged('Skipping existing directory')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_directory(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        test_directory = os.path.join(self.build_dir, 'directory1')
        os.mkdir(test_directory)
        os.chmod(test_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT
        )
        assert self.exists('directory1', type='dir')
        assert get_permissions(test_directory) == 0o775
        assert self.logged('Updating permissions of directory')

    def test_policy_overwrite_directory(self):
        os.mkdir(self.build_dir)
        test_directory = os.path.join(self.build_dir, 'directory1')
        os.mkdir(test_directory)
        os.chmod(test_directory, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE
        )
        assert self.exists('directory1', type='dir')
        assert get_permissions(test_directory) == 0o775
        assert self.logged('Updating permissions of directory')

    def test_skip_identical_directory(self):
        os.mkdir(self.build_dir)
        test_directory = os.path.join(self.build_dir, 'directory1')
        os.mkdir(test_directory)
        os.chmod(
            test_directory,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
            stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
            stat.S_IROTH | stat.S_IXOTH
        )
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True
        )
        assert self.exists('directory1', type='dir')
        assert get_permissions(test_directory) == 0o775
        assert self.logged('Skipping identical directory')

    def test_skip_non_directory(self):
        os.mkdir(self.build_dir)
        replace_dir = os.path.join(self.build_dir, 'directory1')
        open(replace_dir, 'w').close()
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('directory1', type='file')
        assert self.logged('Skipping existing non-directory', level='error')

    # ------------------------------------------------------------------------
    # Test Symbolic Links
    # ------------------------------------------------------------------------
    def test_symlinks_dir_valid(self):
        self.build_scaffold('test-template-2')
        assert self.exists('directory1', type='dir')
        assert self.exists('directory2', type='dir')
        assert self.exists('symlinkc', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkc')) ==
            'directory1'
        )

    def test_symlinks_dir_invalid(self):
        self.build_scaffold('test-template-2')
        assert self.exists('directory1', type='dir')
        assert self.exists('directory2', type='dir')
        assert self.exists('symlinkd', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkd')) == 'baddir'
        )

    def test_symlinks_file_valid(self):
        self.build_scaffold('test-template-2')
        assert self.exists('filea.txt', type='file')
        assert self.exists('fileb.txt', type='file')
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'filea.txt'
        )

    def test_symlinks_file_invalid(self):
        self.build_scaffold('test-template-2')
        assert self.exists('filea.txt', type='file')
        assert self.exists('fileb.txt', type='file')
        assert self.exists('symlinkb.html', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkb.html')) ==
            'badfile.txt'
        )

    def test_symlink_template_extension(self):
        self.build_scaffold('test-template-2', template_extension='html')
        assert self.exists('filea.txt', type='file')
        assert self.exists('fileb.txt', type='file')
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'filea.txt'
        )
        assert self.exists('symlinkb', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkb')) ==
            'badfile.txt'
        )

    def test_policy_skip_symlink(self):
        os.mkdir(self.build_dir)
        os.symlink('saywhat', os.path.join(self.build_dir, 'symlinka.txt'))
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_SKIP
        )
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'saywhat'
        )
        assert self.logged('Skipping existing symlink')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=False)
    def test_policy_prompt_no_symlink(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        os.symlink('saywhat', os.path.join(self.build_dir, 'symlinka.txt'))
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT
        )
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'saywhat'
        )
        assert self.logged('Skipping existing symlink')

    @mock.patch('flaskage.scaffold.prompt_yes_no', return_value=True)
    def test_policy_prompt_yes_symlink(self, mock_prompt_yes_no):
        os.mkdir(self.build_dir)
        os.symlink('saywhat', os.path.join(self.build_dir, 'symlinka.txt'))
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_PROMPT
        )
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'filea.txt'
        )
        assert self.logged('Creating and overwriting symlink')

    def test_policy_overwrite_symlink(self):
        os.mkdir(self.build_dir)
        os.symlink('saywhat', os.path.join(self.build_dir, 'symlinka.txt'))
        self.build_scaffold(
            'test-template-2', overwrite_target_root=True,
            existing_policy=Scaffold.EXISTING_OVERWRITE
        )
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'filea.txt'
        )
        assert self.logged('Creating and overwriting symlink')

    def test_skip_identical_symlink(self):
        os.mkdir(self.build_dir)
        os.symlink('filea.txt', os.path.join(self.build_dir, 'symlinka.txt'))
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('symlinka.txt', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinka.txt')) ==
            'filea.txt'
        )
        assert self.exists('symlinkb.html', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkb.html')) ==
            'badfile.txt'
        )
        assert self.exists('symlinkc', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkc')) ==
            'directory1'
        )
        assert self.exists('symlinkd', type='link')
        assert (
            os.readlink(os.path.join(self.build_dir, 'symlinkd')) == 'baddir'
        )
        assert self.logged('Skipping identical symlink')

    def test_skip_non_symlink(self):
        os.mkdir(self.build_dir)
        replace_symlink = os.path.join(self.build_dir, 'symlinkc')
        open(replace_symlink, 'w').close()
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('symlinkc', type='file')
        assert self.logged('Skipping existing non-symlink', level='error')
