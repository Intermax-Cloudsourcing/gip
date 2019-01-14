class ArchiveNotFound(Exception):
    """ Exception thrown when archive not found

        Attributes:
            repo -- url of the repository
    """

    def __init__(self, repo, version):
        self.repo = repo
        self.version = version

    def __str__(self):
        return "Archive not found: {repo}@{version}".format(
            repo=self.repo,
            version=self.version)


class RepoNotFound(Exception):
    """ Exception thrown when repository not found

        Attributes:
            repo -- url of the repository
    """

    def __init__(self, repo):
        self.repo = repo

    def __str__(self):
        return "Repository not found: {repo}".format(repo=self.repo)


class ValidationError(Exception):
    """ Exception trown when authentication error with source

        Attributes:
            file -- filename with validation error
            erros -- errors in file as dict
    """

    def __init__(self, file, errors):
        self.file = file
        self.errors = errors

    def __str__(self):
        return "Validation errors in {file}: {errors}".format(file=self.file, errors=self.errors)


class AuthenticationError(Exception):
    """ Exception trown when authentication error with source

        Attributes:
            url -- url of the server
    """

    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "Authentication error with: {url}".format(url=self.url)


class HttpError(Exception):
    """ Exception trown when the return code is not 2xx

        Attributes:
            url -- url of the request
    """

    def __init__(self, url, code=None):
        self.url = url
        self.code = code

    def __str__(self):
        return "Request could not complete for: {url}".format(url=self.url)
