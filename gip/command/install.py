import sys
import click
import logging
import pathlib
from urllib.parse import urlsplit

from gip import logger
from gip import parser
from gip import exceptions
from gip.sources import github, gitlab

LOG = logger.get_logger(__name__)


def _get_base_url(repo):
    """ Return base url of repo url"""
    # Split repo url in parts
    split_url = urlsplit(repo)
    return "{0}://{1}".format(split_url.scheme, split_url.netloc)


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
    # Parse requirements to Python object
    requirements = parser.parse_requirements_file(requirements)

    # Validate requirements
    result = parser.validate_requirements(requirements)
    if result['result'] is False:
        raise exceptions.ValidationError(file=requirements, errors=result['errors'])

    if any(d['type'] == 'gitlab' for d in requirements) and args['gitlab_token'] is None:
        # When a type gitlab is defined token and token not passed
        LOG.error("Gitlab repo in requirements but no token passed, use --gitlab-token")
        return

    if any(d['type'] == 'github' for d in requirements) and args['github_token'] is None:
        # When a type gitlab is defined token and token not passed
        LOG.warn("Github repo in requirements but no token passed. \
                    This could result in rate limiting on the API, use --github-token to mitigate.")

    for requirement in requirements:
        try:
            if requirement['type'] == 'gitlab':
                # Init Gitlab object
                source = gitlab.Gitlab(
                    url=_get_base_url(repo=requirement['repo']),
                    token=args['gitlab_token']
                )
            elif requirement['type'] == 'github':
                # Init Github object
                source = github.Github(
                    token=args['github_token']
                )
        except exceptions.RepoNotFound as e:
            LOG.error(e)
        except exceptions.HttpError as e:
            LOG.error(e)
        except exceptions.AuthenticationError as e:
            LOG.error(e)

        # Convert dest to absolute path
        dest = pathlib.Path(requirement['dest']).resolve()
        archive_name = "{}.zip".format(requirement['name'])
        # Append name to destination directory
        archive_dest = dest.joinpath(archive_name)

        # Get the archive
        try:
            source.get_archive(
                repo=requirement['repo'],
                version=requirement['version'],
                dest=archive_dest
            )
        except exceptions.RepoNotFound as e:
            LOG.error(e)
        except FileNotFoundError:
            LOG.error("Destination directory does not exist")

        # Extract archive to location
        try:
            source.untar_archive(
                src=archive_dest,
                dest=dest,
                name=requirement['name']
            )
        except FileNotFoundError:
            LOG.error("Archive not found: {}".format(archive_dest))
        except TypeError:
            LOG.error("Downloaded archive is not a valid tar archive: {}".format(archive_dest))
