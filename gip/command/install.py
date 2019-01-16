import sys
import click
import logging
import pathlib
from urllib.parse import urlsplit

from gip import logger
from gip import util
from gip import exceptions
from gip import util
from gip.models.requirements import Requirements
from gip.sources import github, gitlab

LOG = logger.get_logger(__name__)


@click.command()
@click.pass_context
@click.option(
    '--requirements',
    '-r',
    help='Requirements file to install')
def install(ctx, requirements):
    """
    Install dependencies
    """
    args = ctx.obj.get('args')

    # Set passed requirement path as variable
    requirements_path = requirements

    # Parse requirements to Python object
    try:
        requirements = Requirements(util.read_yaml(path=requirements_path))
    except exceptions.ParserError as e:
        util.sysexit_with_message(e)

    # Validate requirements
    try:
        Requirements.validate(requirements=requirements)
    except exceptions.ValidationError as e:
        util.sysexit_with_message("Parsing failed for {file} due to {errors}".format(
            file=requirements_path,
            errors=e.error
        ))

    # After parsing check if a token is mandatory or advised
    if any(d['type'] == 'gitlab' for d in requirements) and args['gitlab_token'] is None:
        util.sysexit_with_message("Gitlab repo in requirements but no token passed, use --gitlab-token")
    if any(d['type'] == 'github' for d in requirements) and args['github_token'] is None:
        LOG.warn("Github repo in requirements but no token passed. \
                    This could result in rate limiting on the API, use --github-token to mitigate.")

    # Init lockfile
    lock_file = pathlib.Path(args['lock_file'])
    if lock_file.is_file():
        current_lock = util.read_yaml(args['lock_file'])
    else:
        LOG.info("Lock file does not exist, will be created at {path}".format(path=lock_file))

    # Loop requirements for downloading
    new_lock = []
    for requirement in requirements:
        try:
            if requirement['type'] == 'gitlab':
                # Init Gitlab object
                source = gitlab.Gitlab(
                    repo=requirement['repo'],
                    version=requirement['version'],
                    token=args['gitlab_token']
                )
            elif requirement['type'] == 'github':
                # Init Github object
                source = github.Github(
                    repo=requirement['repo'],
                    version=requirement['version'],
                    token=args['github_token']
                )
        except exceptions.RepoNotFound as e:
            LOG.error(e)
        except exceptions.HttpError as e:
            LOG.error(e)
        except exceptions.AuthenticationError as e:
            LOG.error(e)

        # if source.get_commit_hash() != lock_file['']:
        # Convert dest to absolute path
        dest = pathlib.Path(requirement['dest']).resolve()
        archive_name = "{}.zip".format(requirement['name'])
        # Append name to destination directory
        archive_dest = dest.joinpath(archive_name)

        # Get the archive
        try:
            source.get_archive(
                dest=archive_dest
            )
        except FileNotFoundError:
            # Write current state to lock
            _write_lock_file(
                path=lock_file,
                current_lock=current_lock,
                new_lock=new_lock
            )
            util.sysexit_with_message(
            "Destination directory for {name} ({dest}) does not exist".format(
                name=requirement['name'],
                dest=requirement['dest']
            ))

        # Extract archive to location
        try:
            source.untar_archive(
                src=archive_dest,
                dest=dest,
                name=requirement['name']
            )
        except FileNotFoundError:
            _write_lock_file(
                path=lock_file,
                current_lock=current_lock,
                new_lock=new_lock
            )
            util.sysexit_with_message(
                "Archive not found: {}".format(archive_dest))
        except TypeError:
            # Remove archive
            util.remove_file(archive_dest)
            # Write current state to lock
            _write_lock_file(
                path=lock_file,
                current_lock=current_lock,
                new_lock=new_lock
            )
            util.sysexit_with_message(
                "Downloaded archive is not a valid tar archive: {}".format(archive_dest))
        except exceptions.DirectoryNotEmpty as e:
            # Remove archive
            util.remove_file(archive_dest)
            # Write current state to lock
            _write_lock_file(
                path=lock_file,
                current_lock=current_lock,
                new_lock=new_lock
            )
            util.sysexit_with_message(e)

        # No exceptions add to new_lock since succesfull download
        new_lock.append(
            name=requirement['name'],
            version=source.get_commit_hash()
        )

    # End for loop
    _write_lock_file(
        path=lock_file,
        current_lock=current_lock,
        new_lock=new_lock
    )

def _write_lock_file(path, current_lock, new_lock):
    """
    Write current state to lock file
    """
    # No current lock just write to file
    if current_lock is False:
        util.write_yaml(
            path=path,
            data=current_lock
        )
    else:
        # Current lock, merge the two and write to file
        print()


# TODO: Implement this to keep the exception handling more readable
# def _cleanup_and_exit(exception, archive=None):
#     if archive:
#         # Remove archive
#         util.remove_file(archive)

#     # Write current state to lock
#     _write_lock_file(
#         path=lock_file,
#         current_lock=current_lock,
#         new_lock=new_lock
#     )
#     util.sysexit_with_message(exception)
