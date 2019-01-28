import gitlab
from urllib.parse import urlsplit

from gip import logger
from gip import exceptions
from gip.sources import base

LOG = logger.get_logger(__name__)


class Gitlab(base.Source):
    """ Gitlab source """

    def __init__(self, repo, version, token):
        # Set constants
        self.version = version

        # Init Gitlab connection
        try:
            self.gl = gitlab.Gitlab(
                url=self._get_base_url(repo),
                private_token=token
            )
        except gitlab.GitlabAuthenticationError:
            raise exceptions.AuthenticationError(url=repo)
        except gitlab.GitlabHttpError as e:
            raise exceptions.HttpError(url=repo, code=e.response_code)

        # Split project_path from passed repo url
        project_path = self._get_project_path(repo)

        # Get project from Gitlab API as object
        try:
            self.project = self.gl.projects.get(project_path)
        except gitlab.exceptions.GitlabGetError:
            raise exceptions.RepoNotFound(repo)

    def get_archive(self, dest):
        """ Downloads archive in dest_dir"""
        # Get project archive
        try:
            with open(dest, "wb") as f:
                self.project.repository_archive(
                    sha=self.version, streamed=True, action=f.write)
        except gitlab.GitlabAuthenticationError:
            raise exceptions.AuthenticationError(url=self.project.web_url)
        except gitlab.GitlabListError:
            raise exceptions.ArchiveNotFound(
                repo=self.project.web_url,
                version=self.version
            )

    def get_commit_hash(self):
        """ Get commit hash for this source """
        commits = self.project.commits.list(ref_name=self.version)
        return commits[0].id

    def _get_project_path(self, repo):
        """ Returns project path of repo url """
        # Removes leading slash
        path = urlsplit(repo).path[1:]
        if path[-4:] == ".git":
            # Remove .git from URL
            path = path[:-4]
        return path

    def _get_base_url(self, repo):
        """ Return base url of repo url"""
        # Split repo url in parts
        split_url = urlsplit(repo)
        return "{0}://{1}".format(split_url.scheme, split_url.netloc)
