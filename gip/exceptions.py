class ValidationError(Exception):
    """ Exception thrown when repository not found

        Attributes:
            repo -- url of the repository
    """

    def __init__(self, file, errors):
        self.file = file
        self.errors = errors

    def __str__(self):
        return "Validation errors in {file}: {errors}".format(file=self.file, errors=self.errors)
