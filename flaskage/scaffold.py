# -*- coding: utf-8 -*-
import os
import re
import codecs
import logging
from shutil import copy2

from jinja2 import Environment, StrictUndefined

from .utils import (
    matches_any, get_permissions, md5file, md5data, prompt_yes_no
)


class ScaffoldException(Exception):
    pass


class Scaffold(object):

    EXISTING_SKIP = 1
    EXISTING_PROMPT = 2
    EXISTING_OVERWRITE = 3

    def __init__(
        self, source_root, target_root, variables={},
        overwrite_target_root=False, existing_policy=None,
        ignored_files=[], ignored_dirs=[], template_extension='.jinja',
        jinja2_env=Environment(
            block_start_string='{{%', block_end_string='%}}',
            variable_start_string='{{{', variable_end_string='}}}',
            trim_blocks=True, undefined=StrictUndefined
        )
    ):
        # Essential information providing the template source, destination and
        # related variables in the form of a dict
        self.source_root = source_root
        self.target_root = target_root
        self.variables = variables

        # Overwrite policies for root directory and files
        self.overwrite_target_root = overwrite_target_root
        self.existing_policy = (
            existing_policy if existing_policy else self.EXISTING_PROMPT
        )

        # Lists of ignored files and directories
        self.ignored_files = ignored_files
        self.ignored_dirs = ignored_dirs

        # Jinja2 related settings
        if (
            template_extension is None or
            template_extension.startswith('.')
        ):
            self.template_extension = template_extension
        else:
            self.template_extension = '.' + template_extension
        self.jinja2_env = jinja2_env

        # Create the logger
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def render_structure(self):
        # Render the target root directory using variables
        target_root_render = self.render_filename(self.target_root)

        # Create the destination directory if necessary
        if (
            os.path.exists(target_root_render) and
            not self.overwrite_target_root
        ):
            raise ScaffoldException(
                'The target root directory %s already exists' %
                target_root_render
            )
        elif not os.path.exists(target_root_render):
            self.logger.info(
                'Making root directory %s', target_root_render,
                extra={'action': 'mkdir'}
            )
            os.mkdir(target_root_render)
        else:
            self.logger.info(
                'Skipping existing target root directory %s',
                target_root_render, extra={'action': 'skip'}
            )

        # Walk through each directory in the source root
        for source_dir, local_dirs, local_files in os.walk(
            self.source_root, topdown=True
        ):
            # Exclude any ignored directories
            local_dirs[:] = [d for d in local_dirs
                             if not matches_any(d, self.ignored_dirs)]
            local_dirs.sort()

            # Determine the current target directory we're working in
            target_dir = os.path.abspath(
                os.path.join(
                    target_root_render,
                    os.path.relpath(source_dir, self.source_root)
                )
            )

            # Render the target directory using variables
            target_dir_render = self.render_filename(target_dir)

            # Iterate through each file in the current directory
            for local_file in local_files:

                # Exclude any ignored files
                if matches_any(local_file, self.ignored_files):
                    continue

                source_file = os.path.join(source_dir, local_file)

                # Render the current file into the output directory
                if os.path.islink(source_file):
                    self.render_symlink(
                        source_symlink=source_file,
                        target_dir=target_dir_render
                    )
                else:
                    self.render_file(
                        source_file=source_file,
                        target_dir=target_dir_render
                    )

            local_dirs_valid = []

            # Iterate through each directory in the current directory
            for local_dir in local_dirs:

                source_subdir = os.path.join(source_dir, local_dir)

                # Render the current directory into the output directory
                if os.path.islink(source_subdir):
                    self.render_symlink(
                        source_symlink=source_subdir,
                        target_dir=target_dir_render
                    )
                else:
                    success = self.render_directory(
                        source_subdir=source_subdir,
                        target_dir=target_dir_render
                    )
                    # If None has been returned, then the directory was
                    # created and can be walked.
                    if success is None:
                        local_dirs_valid.append(local_dir)

            local_dirs[:] = local_dirs_valid

    def render_directory(self, source_subdir, target_dir):
        # Get the basename of the source file
        target_subdir = os.path.basename(source_subdir)

        # Render the full target path using variables
        target_path_render = os.path.join(
            target_dir, self.render_filename(target_subdir)
        )

        # Destination exists and is not a regular directory
        if (
            os.path.lexists(target_path_render) and
            not os.path.isdir(target_path_render)
        ):
            self.logger.error(
                'Skipping existing non-directory %s', target_path_render,
                extra={'action': 'skip'}
            )
            return False

        # Destination exists and is identical to source
        if (
            os.path.isdir(target_path_render) and
            get_permissions(source_subdir) ==
            get_permissions(target_path_render)
        ):
            self.logger.info(
                'Skipping identical directory %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Destination exists and policy is "skip"
        if (
            os.path.isdir(target_path_render) and
            self.existing_policy == self.EXISTING_SKIP
        ):
            self.logger.info(
                'Skipping existing directory %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # If we have gotten this far, then we have to deal with the following:
        # * Destination does exist and differs from source
        #   * EXISTING_PROMPT policy
        #     * Destination only has different permissions to source
        #   * EXISTING_OVERWRITE policy
        # * Destination doesn't exist and must be created

        # Create a variable to track whether a permission update has been
        # requested for an existing directory.  This will be None if the
        # destination doesn't exist.
        update_permissions = None

        # Prompt the user to update permissions or overwrite the directory
        # if necessary
        if (
            os.path.isdir(target_path_render) and
            self.existing_policy == self.EXISTING_OVERWRITE
        ):
            update_permissions = True
        elif (
            os.path.isdir(target_path_render) and
            self.existing_policy == self.EXISTING_PROMPT
        ):
            # Destination exists and has different permissions to source
            update_permissions = prompt_yes_no(
                'Update permissions of directory %s to %o?' %
                (target_path_render, get_permissions(source_subdir)),
                default='n'
            )

        # If the user has been prompted to make a change and answered no,
        # then we bail
        if update_permissions is False:
            self.logger.info(
                'Skipping existing directory %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Log the appropriate message depending on the action
        if os.path.isdir(target_path_render):
            self.logger.info(
                'Updating permissions of directory %s to %o',
                target_path_render, get_permissions(source_subdir),
                extra={'action': 'chmod (o)'}
            )
        else:
            self.logger.info(
                'Making directory %s', target_path_render,
                extra={'action': 'mkdir'}
            )

        # Take the appropriate actions
        if update_permissions is None:
            os.mkdir(target_path_render)
        os.chmod(target_path_render, get_permissions(source_subdir))

    def render_symlink(self, source_symlink, target_dir):
        # Get the basename of the source file
        target_symlink = os.path.basename(source_symlink)

        # Strip the extension if necessary
        if (
            self.template_extension is not None and
            target_symlink.endswith(self.template_extension)
        ):
            target_symlink = target_symlink.split(self.template_extension)[0]

        # Render the full target path using variables
        target_path_render = os.path.join(
            target_dir, self.render_filename(target_symlink)
        )

        # Destination exists and is not a symbolic link
        if (
            os.path.exists(target_path_render) and
            not os.path.islink(target_path_render)
        ):
            self.logger.error(
                'Skipping existing non-symlink %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Destination exists and is identical to source
        if (
            os.path.islink(target_path_render) and
            os.readlink(source_symlink) == os.readlink(target_path_render)
        ):
            self.logger.info(
                'Skipping identical symlink %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Destination exists and policy is "skip"
        if (
            os.path.islink(target_path_render) and
            self.existing_policy == self.EXISTING_SKIP
        ):
            self.logger.info(
                'Skipping existing symlink %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # If we have gotten this far, then we have to deal with the following:
        # * Destination does exist and differs from source
        #   * EXISTING_PROMPT policy
        #     * Destination has different content to source
        #   * EXISTING_OVERWRITE policy
        # * Destination doesn't exist and must be created

        # Create a variable to track whether an overwrite has been requested
        # for an existing symlink.  This will be None if the destination
        # doesn't exist.
        overwrite = None

        # Prompt the user to overwrite the symlink if necessary
        if (
            os.path.islink(target_path_render) and
            self.existing_policy == self.EXISTING_OVERWRITE
        ):
            overwrite = True
        elif (
            os.path.islink(target_path_render) and
            self.existing_policy == self.EXISTING_PROMPT
        ):
            overwrite = prompt_yes_no(
                'Overwrite symlink %s?' % target_path_render, default='n'
            )

        # If the user has been prompted to make a change and answered no,
        # then we bail
        if overwrite is False:
            self.logger.info(
                'Skipping existing symlink %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Log the appropriate message depending on the action
        if os.path.islink(target_path_render):
            self.logger.info(
                'Creating and overwriting symlink %s to %s',
                os.path.relpath(source_symlink, self.source_root),
                target_path_render, extra={'action': 'symlink (o)'}
            )
        else:
            self.logger.info(
                'Creating symlink %s to %s',
                os.path.relpath(source_symlink, self.source_root),
                target_path_render, extra={'action': 'symlink'}
            )

        # Take the appropriate actions
        if overwrite is True:
            os.remove(target_path_render)
        os.symlink(os.readlink(source_symlink), target_path_render)

    def render_file(self, source_file, target_dir):
        # Get the basename of the source file
        target_file = os.path.basename(source_file)

        # Assume the source file is not a Jinja2 template
        source_file_template = False

        # Strip the extension and determine if the source is a template
        if self.template_extension is None:
            source_file_template = True
        elif target_file.endswith(self.template_extension):
            source_file_template = True
            target_file = target_file.split(self.template_extension)[0]

        # Render the full target path using variables
        target_path_render = os.path.join(
            target_dir, self.render_filename(target_file)
        )

        # Destination exists and is not a regular file
        if (
            os.path.lexists(target_path_render) and
            not os.path.isfile(target_path_render)
        ):
            self.logger.error(
                'Skipping existing non-file %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Render the source file using Jinja2 if it's a template
        if source_file_template:
            with codecs.open(source_file, 'r', 'utf-8') as f:
                source_file_output = f.read()
                output_render = self.jinja2_env.from_string(
                    source_file_output
                ).render(self.variables)

                # Append newline due to jinja2 bug, see
                # https://github.com/iElectric/mr.bob/issues/30
                if (
                    source_file_output.endswith('\n') and
                    not output_render.endswith('\n')
                ):
                    output_render += '\n'

        # If the destination exists, calculate MD5 and permission details
        # of both the source and destination for comparison
        if os.path.isfile(target_path_render):
            if source_file_template:
                source_file_content = md5data(output_render)
            else:
                source_file_content = md5file(source_file)
            source_file_permissions = get_permissions(source_file)
            target_path_content = md5file(target_path_render)
            target_path_permissions = get_permissions(target_path_render)

        # Destination exists and is identical to source
        if (
            os.path.isfile(target_path_render) and
            source_file_content == target_path_content and
            source_file_permissions == target_path_permissions
        ):
            self.logger.info(
                'Skipping identical file %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Destination exists and policy is "skip"
        if (
            os.path.isfile(target_path_render) and
            self.existing_policy == self.EXISTING_SKIP
        ):
            self.logger.info(
                'Skipping existing file %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # If we have gotten this far, then we have to deal with the following:
        # * Destination does exist and differs from source
        #   * EXISTING_PROMPT policy
        #     * Destination has different content to source
        #     * Destination only has different permissions to source
        #       (same content)
        #   * EXISTING_OVERWRITE policy
        # * Destination doesn't exist and must be created

        # Create some variables to track whether an overwrite or permission
        # update has been requested for an existing file.  These will be
        # None if the destination doesn't exist.
        overwrite = None
        update_permissions = None

        # Prompt the user to update permissions or overwrite the file
        # if necessary
        if (
            os.path.isfile(target_path_render) and
            self.existing_policy == self.EXISTING_OVERWRITE
        ):
            if source_file_content != target_path_content:
                overwrite = True
            else:
                update_permissions = True
        elif (
            os.path.isfile(target_path_render) and
            self.existing_policy == self.EXISTING_PROMPT
        ):
            # Destination exists and has different content to source
            if source_file_content != target_path_content:
                overwrite = prompt_yes_no(
                    'Overwrite file %s?' % target_path_render, default='n'
                )

            # Destination exists and has different permissions to source
            else:
                update_permissions = prompt_yes_no(
                    'Update permissions of file %s to %o?' %
                    (target_path_render, get_permissions(source_file)),
                    default='n'
                )

        # If the user has been prompted to make a change and answered no,
        # then we bail
        if overwrite is False or update_permissions is False:
            self.logger.info(
                'Skipping existing file %s', target_path_render,
                extra={'action': 'skip'}
            )
            return

        # Log the appropriate message depending on the action
        if source_file_template:
            if overwrite is True:
                self.logger.info(
                    'Rendering and overwriting template %s to %s',
                    os.path.relpath(source_file, self.source_root),
                    target_path_render, extra={'action': 'render (o)'}
                )
            elif update_permissions is True:
                self.logger.info(
                    'Updating permissions of template %s to %o',
                    target_path_render, get_permissions(source_file),
                    extra={'action': 'chmod (o)'}
                )
            else:
                self.logger.info(
                    'Rendering template %s to %s',
                    os.path.relpath(source_file, self.source_root),
                    target_path_render, extra={'action': 'render'}
                )
        else:
            if overwrite is True:
                self.logger.info(
                    'Copying and overwriting file %s to %s',
                    os.path.relpath(source_file, self.source_root),
                    target_path_render, extra={'action': 'copy (o)'}
                )
            elif update_permissions is True:
                self.logger.info(
                    'Updating permissions of file %s to %o',
                    target_path_render, get_permissions(source_file),
                    extra={'action': 'chmod (o)'}
                )
            else:
                self.logger.info(
                    'Copying file %s to %s',
                    os.path.relpath(source_file, self.source_root),
                    target_path_render, extra={'action': 'copy'}
                )

        # Take the appropriate actions
        if update_permissions is None:
            if source_file_template:
                with codecs.open(target_path_render, 'w', 'utf-8') as target:
                    target.write(output_render)
            else:
                copy2(source_file, target_path_render)
        os.chmod(target_path_render, get_permissions(source_file))

    def render_filename(self, filename):
        # Go through each filename and replace each of the variables
        variables_regex = re.compile(r'\+[^+%s]+\+' % re.escape(os.sep))
        for replaceable in variables_regex.findall(filename):
            # Remove special + symbols from the current name
            actual_replaceable = replaceable.replace('+', '')

            # Replace the variable with that in our variables dict
            if actual_replaceable in self.variables:
                filename = filename.replace(
                    replaceable, self.variables[actual_replaceable]
                )
            else:
                raise ScaffoldException(
                    '%s variable in filename %s was not found in %s' %
                    (actual_replaceable, filename, self.variables)
                )
        return filename
