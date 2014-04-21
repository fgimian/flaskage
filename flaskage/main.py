#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import argparse
import logging

import flaskage
from flaskage.scaffold import Scaffold, ScaffoldException


def valid_project_directory():
    cwd = os.getcwd()
    return (
        os.path.isdir(os.path.join(cwd, 'application')) and
        os.path.isdir(os.path.join(cwd, 'application', 'assets')) and
        os.path.isdir(os.path.join(cwd, 'application', 'models')) and
        os.path.isdir(os.path.join(cwd, 'application', 'static')) and
        os.path.isdir(os.path.join(cwd, 'application', 'templates')) and
        os.path.isdir(os.path.join(cwd, 'application', 'vendor')) and
        os.path.isdir(os.path.join(cwd, 'application', 'views')) and
        os.path.isdir(os.path.join(cwd, 'migrations')) and
        os.path.isdir(os.path.join(cwd, 'libraries')) and
        os.path.isdir(os.path.join(cwd, 'tests')) and
        os.path.isfile(os.path.join(cwd, 'config.py')) and
        os.path.isfile(os.path.join(cwd, 'manage.py'))
    )


def valid_module_name(s):
    return re.match(r'^[a-z_][a-z0-9_]*$', s)


def camelcase(s):
    return ''.join([i.title() or '_' for i in s.split('_')])


def main():
    # Main parser
    parser_main = argparse.ArgumentParser(
        description='Provides the ability to create parts of a Flaskage '
                    'application.'
    )
    subparsers_main = parser_main.add_subparsers(dest='subparser_main_name')

    # Parser for the new command
    parser_new = subparsers_main.add_parser(
        'new', aliases=['n'],
        help='create a new Flaskage project'
    )
    parser_new.add_argument(
        'name', help='the project name in lowercase underscore format'
    )

    # Parser for the generate command
    parser_generate = subparsers_main.add_parser(
        'generate', aliases=['g'],
        help='generate code for an application component'
    )
    subparsers_generate = (
        parser_generate.add_subparsers(dest='subparser_generate_name')
    )

    # Parser for the generate / asset command
    parser_generate_asset = subparsers_generate.add_parser(
        'asset', aliases=['a'],
        help='create a new set of LESS and Coffeescript assets'
    )
    parser_generate_asset.add_argument(
        'name', help='the asset name in lowercase underscore format'
    )

    # Parser for the generate / blueprint command
    parser_generate_blueprint = subparsers_generate.add_parser(
        'blueprint', aliases=['b'],
        help='create a new application component (blueprint)'
    )
    parser_generate_blueprint.add_argument(
        'name', help='the blueprint name in lowercase underscore format'
    )

    # Parser for the generate / model command
    parser_generate_model = subparsers_generate.add_parser(
        'model', aliases=['m'],
        help='create a new database model'
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
        'library', aliases=['l'],
        help='create a new independent library which is used by your project'
    )
    parser_generate_library.add_argument(
        'name', help='the library name in lowercase underscore format'
    )

    args = parser_main.parse_args()

    # Determine the location of our templates
    template_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(flaskage.__file__), 'templates'
        )
    )

    # Adjust logging output
    logging.basicConfig(format='%(levelname)s [%(action)s]: %(message)s')

    # Setup our ignored directories and files
    ignored_dirs = ['__pycache__']
    ignored_files = ['*.pyc']

    # Validate the name argument (common to all commands)
    if not valid_module_name(args.name):
        parser_main.error(
            'The name provided was not a valid Python module name'
        )
    name_camelcase = camelcase(args.name)

    # Handle CLI choices
    if args.subparser_main_name in ['new', 'n']:
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
            print(
                'Successfully created new project structure'
            )
            print()
        except ScaffoldException as e:
            print()
            print('Error: %s' % e)
            print()

    elif args.subparser_main_name in ['generate', 'g']:
        # Generation of items can only run in a valid project directory
        if not valid_project_directory():
            parser_main.error(
                'You can only run the generate command from a valid project '
                'directory'
            )

        if args.subparser_generate_name in ['asset', 'a']:
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
                print(
                    'Successfully created new asset'
                )
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()

        elif args.subparser_generate_name in ['blueprint', 'b']:
            # Generate the scaffolding for a new blueprint
            print()
            print('Generating new blueprint named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=os.path.join(template_dir, 'blueprint'),
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print(
                    'Successfully created new blueprint'
                )
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()

        elif args.subparser_generate_name in ['model', 'm']:
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
                primary_key_provided = False
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
                print(
                    'Successfully created new model'
                )
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()

        elif args.subparser_generate_name in ['library', 'l']:
            # Generate the scaffolding for a new library
            print()
            print('Generating new library named %s' % args.name)
            print()
            try:
                scaffold = Scaffold(
                    source_root=os.path.join(template_dir, 'library'),
                    target_root=os.getcwd(),
                    variables={
                        'name': args.name, 'name_camelcase': name_camelcase
                    },
                    ignored_dirs=ignored_dirs, ignored_files=ignored_files,
                    overwrite_target_root=True
                )
                scaffold.render_structure()
                print()
                print(
                    'Successfully created new library'
                )
                print()
            except ScaffoldException as e:
                print()
                print('Error: %s' % e)
                print()


if __name__ == '__main__':
    main()
