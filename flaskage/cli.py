#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import logging

import click
from painter import paint

import flaskage
from flaskage.scaffold import Scaffold
from flaskage.utils import camelcase, AliasedGroup, MODULE_NAME
from flaskage.helpers import (
    valid_project_directory, ColoredFormatter, PROJECT_NAME, MODEL_COLUMN,
    COLUMN_TYPE_MAPPING, COLUMN_MODIFIER_MAPPING, COLUMN_MODIFIER_PRIMARY_KEY
)


# Determine the location of our templates
TEMPLATE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(flaskage.__file__), 'templates'
    )
)

# Setup our ignored directories and files
IGNORED_DIRS = ['__pycache__']
IGNORED_FILES = ['*.pyc']


def configure_logging():
    """Adjust log output formatting"""
    formatter = ColoredFormatter('%(description)23s : %(destination)s')
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger = logging.getLogger('flaskage.scaffold')
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)


def mode_option(f):
    o1 = click.option('-f', '--force', 'mode',
                      flag_value=Scaffold.EXISTING_OVERWRITE,
                      help='Force overwriting of existing files')
    o2 = click.option('-p', '--prompt', 'mode', default=True,
                      flag_value=Scaffold.EXISTING_PROMPT,
                      help='Prompt to overwrite existing files (default)')
    o3 = click.option('-s', '--skip', 'mode',
                      flag_value=Scaffold.EXISTING_SKIP,
                      help='Skip existing files')
    return o1(o2(o3(f)))


@click.command(add_help_option=False, cls=AliasedGroup)
@click.help_option('-h', '--help')
def cli():
    """The Flaskage command provides the ability to generate components of a
    Flaskage web application."""
    pass


@click.command(add_help_option=False)
@click.help_option('-h', '--help')
@mode_option
@click.argument('project_name', type=PROJECT_NAME)
@click.pass_context
def new(ctx, project_name, mode):
    """Create a new Flaskage project."""
    # Unpack the project directory and name
    name, directory = project_name

    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(name)

    # Generation of a new project can only run outside a valid project
    # directory
    if valid_project_directory(directory):
        ctx.fail('You cannot create a new project inside a project directory')

    click.echo()
    click.echo('Generating new project %s:' % paint.bold(name))
    click.echo()
    scaffold = Scaffold(
        source_root=os.path.join(TEMPLATE_DIR, 'project'),
        target_root=directory,
        variables={'name': name, 'name_camelcase': name_camelcase},
        ignored_dirs=IGNORED_DIRS, ignored_files=IGNORED_FILES,
        overwrite_target_root=True, existing_policy=mode
    )
    scaffold.render_structure()
    click.echo()
    click.echo('Getting started with your project:')
    click.echo()
    click.echo('  1. Change into the new project directory')
    click.echo('     cd %s' % directory)
    click.echo()
    click.echo('  2. Install all client-side components using Bower')
    click.echo('     bower install')
    click.echo()
    click.echo('  3. Install all server-side dependencies using pip')
    click.echo('     pip install -r requirements.txt')
    click.echo()
    click.echo('  4. Start up the development web server')
    click.echo('     ./manage.py server')
    click.echo()
    click.echo('  5. Browse to your new site at http://localhost:5000/')
    click.echo()


@click.command(add_help_option=False, cls=AliasedGroup)
@click.help_option('-h', '--help')
def generate():
    """Generate code for an application component."""
    pass


@click.command(add_help_option=False)
@click.help_option('-h', '--help')
@mode_option
@click.argument('name', type=MODULE_NAME)
@click.pass_context
def asset(ctx, name, mode):
    """Generate a set of assets."""
    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(name)

    # Generation of items can only run in a valid project directory
    if not valid_project_directory():
        ctx.fail(
            'You can only run the generate command from a valid project '
            'directory'
        )

    click.echo()
    click.echo('Generating new asset named %s:' % paint.bold(name))
    click.echo()
    scaffold = Scaffold(
        source_root=os.path.join(TEMPLATE_DIR, 'asset'),
        target_root=os.getcwd(),
        variables={'name': name, 'name_camelcase': name_camelcase},
        ignored_dirs=IGNORED_DIRS, ignored_files=IGNORED_FILES,
        overwrite_target_root=True, existing_policy=mode
    )
    scaffold.render_structure()
    click.echo()


@click.command(add_help_option=False)
@click.help_option('-h', '--help')
@mode_option
@click.argument('name', type=MODULE_NAME)
@click.pass_context
def blueprint(ctx, name, mode):
    """Generate an application component (blueprint)."""
    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(name)

    # Generation of items can only run in a valid project directory
    if not valid_project_directory():
        ctx.fail(
            'You can only run the generate command from a valid project '
            'directory'
        )

    click.echo()
    click.echo('Generating new blueprint named %s:' % paint.bold(name))
    click.echo()
    scaffold = Scaffold(
        source_root=[
            os.path.join(TEMPLATE_DIR, 'asset'),
            os.path.join(TEMPLATE_DIR, 'blueprint'),
        ],
        target_root=os.getcwd(),
        variables={'name': name, 'name_camelcase': name_camelcase},
        ignored_dirs=IGNORED_DIRS, ignored_files=IGNORED_FILES,
        overwrite_target_root=True, existing_policy=mode
    )
    scaffold.render_structure()
    click.echo()
    click.echo('Steps required to activate the new blueprint:')
    click.echo()
    click.echo('  Add the blueprint import to app/__init__.py in the '
               'configure_blueprints function')
    click.echo()
    click.echo('  from .views import %s_view' % name)
    click.echo('  app.register_blueprint(%s_view.mod)' % name)
    click.echo()


@click.command(add_help_option=False, short_help='Generate a database model')
@click.help_option('-h', '--help')
@mode_option
@click.argument('name', type=MODULE_NAME)
@click.argument('columns', nargs=-1, type=MODEL_COLUMN)
@click.pass_context
def model(ctx, name, columns, mode):
    """Generate a database model using a given name. You may also specify the
    columns you need following the model name using the format:

    <column>[:<type>[,<length>]][:<modifier>][:<modifier>]...

    e.g.

    flaskage g model user email:string:primary name:string,80:index:required

    The following types are listed below along with their corresponding
    SQLAlchemy mapping:

    Numeric Types:
    - integer (or int): Integer
    - decimal: Numeric
    - float: Float

    Text Types:
    - string (or str): String
    - text: Text

    Date & Time Types:
    - date: Date
    - time: Time
    - datetime: DateTime

    Other Types:
    - binary (or bin): LargeBinary
    - boolean (or bool): Boolean

    The string, text and binary types also accept an optional length.

    The column modifiers available are:
    - index
    - primary
    - required
    - unique

    If no primary key is specified, an primary key integer column named id
    will be created for you.
    """
    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(name)

    # Generation of items can only run in a valid project directory
    if not valid_project_directory():
        ctx.fail(
            'You can only run the generate command from a valid project '
            'directory'
        )

    # Generate the Python code required for each column (this is too
    # tedious to do in templates)
    primary_key_provided = False
    column_definitions = []

    for column_name, type, length, modifiers in columns:
        # Generate the type and its size (if applicable)
        definition = 'db.%s' % COLUMN_TYPE_MAPPING[type]
        if length:
            definition += '(%i)' % length

        # Generate modifiers (primary key, index .etc)
        for modifier in modifiers:
            definition += ', %s' % COLUMN_MODIFIER_MAPPING[modifier]
            if modifier == COLUMN_MODIFIER_PRIMARY_KEY:
                primary_key_provided = True

        column_definitions.append((column_name, definition))

    click.echo()
    click.echo('Generating new model named %s:' % paint.bold(name))
    click.echo()
    scaffold = Scaffold(
        source_root=os.path.join(TEMPLATE_DIR, 'model'),
        target_root=os.getcwd(),
        variables={
            'name': name, 'name_camelcase': name_camelcase,
            'column_definitions': column_definitions,
            'primary_key_provided': primary_key_provided
        },
        ignored_dirs=IGNORED_DIRS, ignored_files=IGNORED_FILES,
        overwrite_target_root=True, existing_policy=mode
    )
    scaffold.render_structure()
    click.echo()
    click.echo('Steps required to activate the new model:')
    click.echo()
    click.echo('  1. Add the model import to app/models/__init__.py')
    click.echo('     from .%s import %s  # noqa' % (name, name_camelcase))
    click.echo()
    click.echo('  2. Add the factory import to tests/factories/__init__.py')
    click.echo('     from .%s_factory import %sFactory  # noqa' %
               (name, name_camelcase))
    click.echo()
    click.echo('  3. Generate a migration to add the new model to your '
               'database')
    click.echo('     ./manage.py db migrate')
    click.echo()
    click.echo('  4. Apply the migration')
    click.echo('     ./manage.py db upgrade')
    click.echo()


@click.command(add_help_option=False)
@click.help_option('-h', '--help')
@mode_option
@click.argument('name', type=MODULE_NAME)
@click.pass_context
def library(ctx, name, mode):
    """Generate an application-agnostic library."""
    # Convert the name to CamelCase for use with class names
    name_camelcase = camelcase(name)

    # Generation of items can only run in a valid project directory
    if not valid_project_directory():
        ctx.fail(
            'You can only run the generate command from a valid project '
            'directory'
        )

    click.echo()
    click.echo('Generating new library named %s:' % paint.bold(name))
    click.echo()
    scaffold = Scaffold(
        source_root=os.path.join(TEMPLATE_DIR, 'lib'),
        target_root=os.getcwd(),
        variables={'name': name, 'name_camelcase': name_camelcase},
        ignored_dirs=IGNORED_DIRS, ignored_files=IGNORED_FILES,
        overwrite_target_root=True, existing_policy=mode
    )
    scaffold.render_structure()
    click.echo()

# Setup the command hierarchy
cli.add_command(new)
cli.add_command(generate)
generate.add_command(asset)
generate.add_command(blueprint)
generate.add_command(model)
generate.add_command(library)

# Setup log formatting and display
configure_logging()


if __name__ == '__main__':
    cli()
