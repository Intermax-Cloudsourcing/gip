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
            errors -- errors as dict
    """

    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return "Validation errors: {errors}".format(errors=self.errors)


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


class DirectoryNotEmpty(Exception):
    """ Exception trown when directory not empty

        Attributes:
            directory -- path of not empty directory
    """

    def __init__(self, directory):
        self.directory = directory

    def __str__(self):
        return "Directory not empty: {directory}".format(
            directory=self.directory
        )


class ParserError(Exception):
    """ Exception trown when parsing does not complete

        Attributes:
            file -- path to file which has errors
            error -- error message of parser
    """

    def __init__(self, file, error):
        self.file = file
        self.error = error

    def __str__(self):
        return "Parsing failed for {file} due to {error}".format(
            file=self.file,
            error=self.error)
