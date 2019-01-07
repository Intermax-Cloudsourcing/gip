import gitlab
import subprocess
import os
from urllib.parse import urlsplit


class Source():
    """ Superclass which interfaces all the sources """

    def get_archive(self, repo, version):
        raise NotImplementedError


class Gitlab(Source):
    def __init__(self, logger, url, token):
        self.logger = logger
        self.gl = gitlab.Gitlab(url, private_token=token)

    def get_archive(self, name, repo, version, dest):
        """ Downloads archive in dest_dir"""
        # Split project_path from passed repo url
        project_path = self._get_project_path_from_url(repo)

        project = self.gl.projects.get(project_path)
        with open(name, "wb") as f:
            project.repository_archive(
                sha=version, streamed=True, action=f.write)
        subprocess.run(["unzip", "-bo", name])
        os.unlink(name)

    def _get_project_path_from_url(self, url):
        # Removes leading slash
        path = urlsplit(url).path[1:]
        if path[-4:] == ".git":
            # Remove .git from URL
            path = path[:-4]
        return path
