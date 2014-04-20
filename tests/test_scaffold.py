# -*- coding: utf-8 -*-
from shutil import rmtree
from tempfile import mkdtemp
import os
import stat

import jinja2
from jinja2 import Environment, StrictUndefined
import mock
from nose.tools import raises

import flaskage
from flaskage.scaffold import Scaffold, ScaffoldException
from flaskage.utils import get_permissions


class TestScaffold:
    def setup(self):
        self.temp_dir = mkdtemp()
        self.build_dir = os.path.join(self.temp_dir, 'test')
        self.templates = os.path.abspath(
            os.path.join(
                os.path.dirname(flaskage.__file__), os.pardir, 'tests',
                'templates'
            )
        )

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

    def test_existing_policy_skip(self):
        pass

    def test_existing_policy_prompt(self):
        pass

    def test_existing_policy_overwrite(self):
        pass

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
    # Test Files
    # ------------------------------------------------------------------------
    def test_file(self):
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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o600'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o664'

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
        assert oct(get_permissions(test_file)) == '0o664'

    def test_skip_non_file(self):
        self.build_scaffold('test-template-2')
        replace_file = os.path.join(self.build_dir, 'filea.txt')
        os.remove(replace_file)
        os.mkdir(replace_file)
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('filea.txt', type='dir')

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
        assert oct(get_permissions(test_directory)) == '0o700'

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
        assert oct(get_permissions(test_directory)) == '0o700'

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
        assert oct(get_permissions(test_directory)) == '0o775'

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
        assert oct(get_permissions(test_directory)) == '0o775'

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
        assert oct(get_permissions(test_directory)) == '0o775'

    def test_skip_non_directory(self):
        self.build_scaffold('test-template-2')
        replace_dir = os.path.join(self.build_dir, 'directory1')
        os.rmdir(replace_dir)
        open(replace_dir, 'w').close()
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('directory1', type='file')

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

    def test_skip_non_symlink(self):
        self.build_scaffold('test-template-2')
        replace_symlink = os.path.join(self.build_dir, 'symlinkc')
        os.remove(replace_symlink)
        open(replace_symlink, 'w').close()
        self.build_scaffold('test-template-2', overwrite_target_root=True)
        assert self.exists('symlinkc', type='file')
