#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import sys
import argparse
import logging

from painter import paint

import flaskage
from flaskage.scaffold import Scaffold, ScaffoldException


def valid_project_directory():
    cwd = os.getcwd()
    return (
        os.path.isdir(os.path.join(cwd, 'app')) and
        os.path.isdir(os.path.join(cwd, 'app', 'assets')) and
        os.path.isdir(os.path.join(cwd, 'app', 'models')) and
        os.path.isdir(os.path.join(cwd, 'app', 'static')) and
        os.path.isdir(os.path.join(cwd, 'app', 'templates')) and
        os.path.isdir(os.path.join(cwd, 'app', 'views')) and
        os.path.isdir(os.path.join(cwd, 'db', 'migrations')) and
        os.path.isdir(os.path.join(cwd, 'vendor', 'assets')) and
        os.path.isdir(os.path.join(cwd, 'lib')) and
        os.path.isdir(os.path.join(cwd, 'tests')) and
        os.path.isfile(os.path.join(cwd, 'config.py')) and
        os.path.isfile(os.path.join(cwd, 'manage.py'))
    )


def valid_module_name(s):
    return re.match(r'^[a-z_][a-z0-9_]*$', s)


def camelcase(s):
    return ''.join([i.title() or '_' for i in s.split('_')])


class ColoredFormatter(logging.Formatter):
    COLOR_MAPPING = {
        'identical': paint.light_blue,
        'exist': paint.light_blue,
        'conflict': paint.light_red,
        'create': paint.light_green,
        'update': paint.light_yellow
    }

    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        if self.use_color:
            color = self.COLOR_MAPPING[record.description]
            record.description = color(record.description)
        return logging.Formatter.format(self, record)


def main():
    # Main parser
    parser_main = argparse.ArgumentParser(
        description='Provides the ability to create parts of a Flaskage '
                    'application.'
    )
    subparsers_main = parser_main.add_subparsers(dest='subparser_main_name')

    # Parser for the new command
    parser_new = subparsers_main.add_parser(
        'new', help='create a new Flaskage project'
    )
    parser_new.add_argument(
        'name', help='the project name in lowercase underscore format'
    )

    # Parser for the generate command
    parser_generate = subparsers_main.add_parser(
        'generate', help='generate code for an application component'
    )
    subparsers_generate = (
        parser_generate.add_subparsers(dest='subparser_generate_name')
    )

    # Parser for the generate / asset command
    parser_generate_asset = subparsers_generate.add_parser(
        'asset', help='create a new set of LESS and Coffeescript assets'
    )
    parser_generate_asset.add_argument(
        'name', help='the asset name in lowercase underscore format'
    )

    # Parser for the generate / blueprint command
    parser_generate_blueprint = subparsers_generate.add_parser(
        'blueprint', help='create a new application component (blueprint)'
    )
    parser_generate_blueprint.add_argument(
        'name', help='the blueprint name in lowercase underscore format'
    )

    # Parser for the generate / model command
    parser_generate_model = subparsers_generate.add_parser(
        'model', help='create a new database model'
    )
    parser_generate_model.add_argument(
        'name', help='the model name in lowercase underscore format'
    )
    parser_generate_model.add_argument(
        'columns', nargs='*',
        help='column definitions for the new model'
    )

    # Parser for the generate / library command
    parser_generate_library = subparsers_generate.add_parser(
        'lib',
        help='create a new independent library which is used by your project'
    )
    parser_generate_library.add_argument(
        'name', help='the library name in lowercase underscore format'
    )

    # Parse the command line arguments
    args = parser_main.parse_args()

    # Print help if no arguments are provided (required on Python 3)
    if not args.subparser_main_name:
        parser_main.print_usage()
        parser_main.exit()
    elif (
        args.subparser_main_name in ['generate'] and
        not args.subparser_generate_name
    ):
        parser_generate.print_usage()
        parser_generate.exit()

    # Determine the location of our templates
    template_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(flaskage.__file__), 'templates'
        )
    )

    # Adjust logging output
    logger = logging.getLogger('flaskage.scaffold')
    logger.setLevel(logging.DEBUG)

    formatter = ColoredFormatter('%(description)23s : %(destination)s')

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    # logging.basicConfig(format='%(description)12s : %(destination)s')

    # Setup our ignored directories and files
    ignored_dirs = ['__pycache__']
    ignored_files = ['*.pyc']

    # Validate the name argument (common to all commands)
    if not valid_module_name(args.name):
        parser_main.error(
            'The name provided was not a valid Python module name'
        )

    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(args.name)

    # Handle the new command
    if args.subparser_main_name in ['new']:
        # Generation of a new project can only run outside a valid project
        # directory
        if valid_project_directory():
            parser_main.error(
                'You cannot create a new project inside a project directory'
            )

        # Generate the scaffolding for a new project
        print()
        print('Generating new project in %s' % args.name)
        print()
        try:
            scaffold = Scaffold(
                source_root=os.path.join(template_dir, 'project'),
                target_root=args.name,
                variables={
                    'name': args.name, 'name_camelcase': name_camelcase
                },
                ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                overwrite_target_root=True
            )
            scaffold.render_structure()
            print()
            print('Successfully created new project structure')
            print()
        except ScaffoldException as e:
            print()
            print('Error: %s' % e)
            print()
            exit(1)

    # Handle the generate command
    elif args.subparser_main_name in ['generate']:
        # Generation of items can only run in a valid project directory
        if not valid_project_directory():
            parser_main.error(
                'You can only run the generate command from a valid project '
                'directory'
            )

        # Handle the generate / asset command
        if args.subparser_generate_name in ['asset']:
            # Generate the scaffolding for a new asset
            print()
            print('Generating new asset named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=os.path.join(template_dir, 'asset'),
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print('Successfully created new asset')
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()
                exit(1)

        # Handle the generate / blueprint command
        elif args.subparser_generate_name in ['blueprint']:
            # Generate the scaffolding for a new blueprint
            print()
            print('Generating new blueprint named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=[
                        os.path.join(template_dir, 'asset'),
                        os.path.join(template_dir, 'blueprint'),
                    ],
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print('Successfully created new blueprint')
                print()
                print(
                    'Add the blueprint import to app/__init__.py in the '
                    'configure_blueprints function'
                )
                print()
                print('    from .views import %s' % args.name)
                print('    app.register_blueprint(%s.mod)' % args.name)
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()
                exit(1)

        # Handle the generate / model command
        elif args.subparser_generate_name in ['model']:
            column_mapping = {
                'integer': 'Integer',
                'decimal': 'Numeric',
                'float': 'Float',
                'boolean': 'Boolean',
                'date': 'Date',
                'time': 'Time',
                'datetime': 'DateTime',
                'binary': 'LargeBinary',
                'string': 'String',
                'text': 'Text'
            }

            primary_key_provided = False
            columns = []
            for column in args.columns:
                column_properties = column.split(':')

                # Extract the column name
                name = column_properties[0]
                if not valid_module_name(name):
                    parser_main.error(
                        'The name provided was not a valid Python module name'
                    )

                # Extract the column type and length
                length = None
                try:
                    type_properties = column_properties[1].split(',')
                    type = type_properties[0].lower() or 'string'
                    try:
                        if type_properties[1]:
                            length = int(type_properties[1])
                        else:
                            length = None
                    except IndexError:
                        length = None
                except IndexError:
                    type = 'string'
                except ValueError:
                    parser_main.error(
                        'The column definition for field %s contained an '
                        'invalid length' % name
                    )
                if type not in [
                    'integer', 'decimal', 'float', 'string', 'text',
                    'datetime', 'date', 'time', 'boolean', 'binary'
                ]:
                    parser_main.error(
                        'The type of column %s must be one of the following:\n'
                        '\n'
                        'Numberic Types:\n'
                        '- integer\n'
                        '- decimal\n'
                        '- float\n'
                        '\n'
                        'Text Types:\n'
                        '- string\n'
                        '- text\n'
                        '\n'
                        'Date & Time Types:\n'
                        '- datetime\n'
                        '- date\n'
                        '- time\n'
                        '\n'
                        'Other Types:\n'
                        '- boolean\n'
                        '- binary\n' % name
                    )
                if length and type not in ['string', 'text', 'binary']:
                    parser_main.error(
                        'The length of column %s is invalid as length can '
                        'only be specified for string, text or binary types' %
                        name
                    )

                # Extract the column modifiers
                try:
                    modifiers = column_properties[2].lower().split(',')
                except IndexError:
                    modifiers = []
                for modifier in modifiers:
                    if modifier not in [
                        'index', 'primary', 'required', 'unique'
                    ]:
                        parser_main.error(
                            'The column modifier for column %s must be one of'
                            'the following:\n'
                            '\n'
                            '- index\n'
                            '- primary\n'
                            '- required\n'
                            '- unique\n' % name
                        )

                definition = 'db.%s' % column_mapping[type]
                if length:
                    definition += '(%i)' % length
                if modifiers:
                    for modifier in modifiers:
                        if modifier == 'index':
                            definition += ', index=True'
                        elif modifier == 'primary':
                            primary_key_provided = True
                            definition += ', primary_key=True'
                        elif modifier == 'required':
                            definition += ', nullable=False'
                        elif modifier == 'unique':
                            definition += ', unique=True'

                columns.append((name, definition))

            # Generate the scaffolding for a new model
            print()
            print('Generating new model named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=os.path.join(template_dir, 'model'),
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase,
                        'columns': columns,
                        'primary_key_provided': primary_key_provided
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print('Successfully created new model')
                print()
                print('1. Add the model import to app/models/__init__.py')
                print()
                print(
                    'from .%s import %s  # noqa' %
                    (args.name, name_camelcase)
                )
                print()
                print(
                    '2. Add the factory import to tests/factories/__init__.py'
                )
                print()
                print(
                    'from .%s import %sFactory  # noqa' %
                    (args.name, name_camelcase)
                )
                print()
                print(
                    '3. Generate a migration to add the new model to your '
                    'database'
                )
                print()
                print('./manage.py db migrate')
                print()
                print('4. Apply the migration')
                print()
                print('./manage.py db upgrade')
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()
                exit(1)

        # Handle the generate / library command
        elif args.subparser_generate_name in ['lib']:
            # Generate the scaffolding for a new library
            print()
            print('Generating new library named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=os.path.join(template_dir, 'lib'),
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print('Successfully created new library')
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()
                exit(1)


if __name__ == '__main__':
    main()
