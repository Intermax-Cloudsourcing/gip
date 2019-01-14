import github3

from gip import logger
from gip import exceptions
from gip.sources import base

LOG = logger.get_logger(__name__)


class Github(base.Source):
    """ Github source """
    def __init__(self, token):
        try:
            self.gh = github3.login(token=token)
        except github3.exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationError(url="https://github.com")

    def get_archive(self, repo, version, dest):
        """ Downloads archive in dest_dir"""
        # Get repository from Gitlab API
        try:
            repository = self.gh.repository(
                owner=self.get_owner(repo),
                repository=self.get_repo_name(repo)
            )
        except github3.exceptions.ConnectionError:
            raise exceptions.HttpError(url=repo)
        except github3.exceptions.NotFoundError:
            raise exceptions.RepoNotFound(repo=repo)

        # Download repository archive to dest
        result = repository.archive(
            format='tarball',
            path=dest,
            ref=version
        )
        if result is False:
            raise exceptions.ArchiveNotFound(repo=repo, version=version)

    def get_owner(self, url):
        """ Get owner name from repo url"""
        # Split owner from url
        owner = url.split("/")[3]
        return owner

    def get_repo_name(self, url):
        """ Get repo name from repo url """
        if url[-4:] == ".git":
            # Remove .git from url
            url = url[:-4]
        # Split repo_name from url
        repo_name = url.split("/")[4]
        return repo_name
