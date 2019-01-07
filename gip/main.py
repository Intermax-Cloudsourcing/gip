import argparse
from pathlib import Path
from urllib.parse import urlsplit

from helpers import Logger, Requirements
from sources import Gitlab

logger = Logger()


class Install(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("pass a requirements.yml file to install")
        super(Install, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        path = Path(values).resolve()
        namespace.requirements = Requirements(str(path), logger).requirements
        self._get_requirements(namespace)

    def _get_requirements(self, namespace):
        for requirement in namespace.requirements:
            if requirement['type'] == 'gitlab':
                # Repo comes from Gitlab, check for API token
                if namespace.gitlab_token:
                    # Split repo url in parts
                    split_url = urlsplit(requirement['repo'])
                    url = "{0}://{1}".format(split_url.scheme, split_url.netloc)
                    # API token defined, init gitlab object
                    gitlab = Gitlab(logger, url, namespace.gitlab_token)
                    # Convert dest to absolute path
                    dest = Path(requirement['dest']).resolve()
                    # Get the archive
                    gitlab.get_archive(
                        name=requirement['name'],
                        repo=split_url.path,
                        version=requirement['version'],
                        dest=dest)
                else:
                    logger.error("No Gitlab API token provided")


parser = argparse.ArgumentParser(
    description='Pip style script for Git releases')
parser.add_argument('install', action=Install,
                    help='the location of the requirements.yml'),
parser.add_argument('--gitlab-token', dest='gitlab_token',
                    help='provide the private token for Gitlab API')
parser.add_argument('--github-token', dest='github_token',
                    help='provide the private token for Github API')
args = parser.parse_args()

print(args)
