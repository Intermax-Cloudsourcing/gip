import gitlab
from urllib.parse import urlsplit

from gip import logger
from gip import exceptions
from gip.sources import base

LOG = logger.get_logger(__name__)


class Gitlab(base.Source):
    """ Gitlab source """

    def __init__(self, url, token):
        try:
            self.gl = gitlab.Gitlab(
                url=url,
                private_token=token
            )
        except gitlab.GitlabAuthenticationError:
            raise exceptions.AuthenticationError(url=url)
        except gitlab.GitlabHttpError as e:
            raise exceptions.HttpError(url=url, code=e.response_code)

    def get_archive(self, repo, version, dest):
        """ Downloads archive in dest_dir"""
        # Split project_path from passed repo url
        project_path = self.get_project_path(repo)

        # Get project from Gitlab API
        try:
            project = self.gl.projects.get(project_path)
        except gitlab.exceptions.GitlabGetError:
            raise exceptions.RepoNotFound(repo)

        # Get project archive
        try:
            with open(dest, "wb") as f:
                project.repository_archive(
                    sha=version, streamed=True, action=f.write)
        except gitlab.GitlabAuthenticationError:
            raise exceptions.AuthenticationError(url=repo)
        except gitlab.GitlabListError:
            raise exceptions.ArchiveNotFound(repo=repo, version=version)

    def get_project_path(self, url):
        """ Returns project path of repo url """
        # Removes leading slash
        path = urlsplit(url).path[1:]
        if path[-4:] == ".git":
            # Remove .git from URL
            path = path[:-4]
        return path
