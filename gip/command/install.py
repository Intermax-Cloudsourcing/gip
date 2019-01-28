import click
import pathlib

from gip import logger
from gip import util
from gip import exceptions
from gip import model
from gip import sources

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
    requirements_path = pathlib.Path(requirements)

    # Parse requirements file to Python object
    if requirements_path.is_file():
        requirements = _parse_and_validate(
            path=requirements_path,
            type='requirements'
        )
    else:
        util.sysexit_with_message("Passed requirement file does not exist: \
        {path}".format(
            path=requirements_path
        ))

    # After parsing check if a token is mandatory or advised
    if (any(d['type'] == 'gitlab' for d in requirements) and
            args['gitlab_token'] is None):
        util.sysexit_with_message(
            "Gitlab repo in requirements but no token passed, \
            use --gitlab-token"
        )
    if (any(d['type'] == 'github' for d in requirements) and
            args['github_token'] is None):
        util.sysexit_with_message(
            "Github repo in requirements but no token passed, \
            use --github-token"
        )

    # Init lockfile
    locks_path = pathlib.Path(args['lock_file'])

    # Init current_lock list
    current_lock = {}
    if locks_path.is_file():
        current_lock = _parse_and_validate(
            path=locks_path,
            type='locks'
        )
    else:
        LOG.info("Lock file does not exist, will be created at {path}".format(
            path=locks_path)
        )

    # Init new_lock list
    new_lock = {}
    # Loop requirements for downloading
    for requirement in requirements:
        if requirement['name'] in current_lock:
            LOG.info("{requirement} already installed, skipping".format(
                requirement=requirement['name'])
            )
        else:
            try:
                if requirement['type'] == 'gitlab':
                    # Init Gitlab object
                    source = sources.gitlab.Gitlab(
                        repo=requirement['repo'],
                        version=requirement['version'],
                        token=args['gitlab_token']
                    )
                elif requirement['type'] == 'github':
                    # Init Github object
                    source = sources.github.Github(
                        repo=requirement['repo'],
                        version=requirement['version'],
                        token=args['github_token']
                    )
            except exceptions.RepoNotFound as e:
                util.sysexit_with_message(e)
            except exceptions.HttpError as e:
                util.sysexit_with_message(e)
            except exceptions.AuthenticationError as e:
                util.sysexit_with_message(e)

            # Convert dest to absolute path
            dest = pathlib.Path(requirement['dest']).resolve()
            # Create archive name (ex. ansible-role-plex.tar.gz)
            archive_name = "{}.tar.gz".format(requirement['name'])
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
                    path=locks_path,
                    current_lock=current_lock,
                    new_lock=new_lock
                )
                util.sysexit_with_message(
                    "Destination directory for {name} ({dest}) \
                    does not exist".format(
                        name=requirement['name'],
                        dest=dest
                    )
                )

            # Extract archive to location
            try:
                source.untar_archive(
                    src=archive_dest,
                    dest=dest,
                    name=requirement['name']
                )
            except Exception as e:
                # Write current state to lock
                _write_lock_file(
                    path=locks_path,
                    current_lock=current_lock,
                    new_lock=new_lock
                )
                # Set better description for generic Python errors
                if type(e) is FileNotFoundError:
                    e = "Archive not found: {archive}".format(
                        archive=archive_dest
                    )
                    util.sysexit_with_message(e)  # No need for remove
                elif type(e) is TypeError:
                    e = "Downloaded archive is not a valid tar archive: \
                    {archive}".format(
                        archive=archive_dest
                    )
                # Cleanup archive
                util.remove_file(archive_dest)
                # Exit with message
                util.sysexit_with_message(e)

            # No exceptions add to new_lock since succesfull download
            LOG.success("{requirement} successfully installed".format(
                    requirement=requirement['name'])
                )
            new_lock[requirement['name']] = source.get_commit_hash()

    # End for loop
    _write_lock_file(
        path=locks_path,
        current_lock=current_lock,
        new_lock=new_lock
    )


def _write_lock_file(path, current_lock, new_lock):
    """
    Write current state to lock file
    """
    # Check if new_lock has data
    if new_lock:
        # No current lock just write to file
        if not current_lock:
            util.write_yaml(
                path=path,
                data=new_lock
            )
        else:
            # Current lock, merge the two and write to file
            util.write_yaml(
                path=path,
                data=util.merge_dicts(current_lock, new_lock)
            )


def _parse_and_validate(path, type):
    """ Parse and validate lock or requirements file """
    try:
        data = util.read_yaml(path=path)
    except exceptions.ParserError as e:
        util.sysexit_with_message(e)

    # Validate requirements file
    try:
        model.scheme.validate(
            type=type,
            data=data
        )
    except exceptions.ValidationError as e:
        util.sysexit_with_message(
            "Parsing failed for {file} due to {errors}".format(
                file=path,
                errors=e.errors
            )
        )

    # Return parsed and validated data
    return data
