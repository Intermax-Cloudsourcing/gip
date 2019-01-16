import cerberus
from gip import exceptions

class Model():
    """ Superclass which interfaces all the models """
    def __init__(self, scheme):
        self.scheme = scheme

    def validate(self, data):
        """
        TODO: Write doc
        """
        validator = cerberus.Validator(self.scheme)
        if validator:
            return True  # Valid data according to scheme
        else:
            raise exceptions.ValidationError(errors=validator.errors)
