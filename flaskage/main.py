#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse

import flaskage
from flaskage.scaffold import Scaffold


def main():
    # Main parser for all Flaskage commands
    parser = argparse.ArgumentParser(
        description='Provides the ability to create parts of a Flaskage '
                    'application.'
    )
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Subparser for the new command
    parser_new = subparsers.add_parser(
        'new', help='create a new Flaskage project'
    )
    parser_new.add_argument(
        'name', help='the project name in lowercase underscore format'
    )

    # Subparser for the generate command
    parser_generate = subparsers.add_parser(
        'generate', help='generate code for an application component'
    )
    parser_generate.add_argument(
        'type', choices=['model', 'blueprint', 'library', 'scaffold']
    )
    parser_generate.add_argument(
        'name', help='the component name in lowercase underscore format'
    )
    parser_generate.add_argument(
        'column', nargs='*',
        help='(model and scaffold only) column definitions for the new model'
    )

    args = parser.parse_args()

    # Determine the location of our templates
    template_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(flaskage.__file__), 'templates'
        )
    )

    if args.subparser_name == 'new':
        scaffold = Scaffold(
            source_root=os.path.join(template_dir, 'project'),
            target_root=args.name,
            variables={'name': args.name},
            overwrite_target_root=True
        )
        scaffold.render_structure()

    # print args.subparser_name
    # print args.type
    # print args.column
    # print args.name


if __name__ == '__main__':
    main()
