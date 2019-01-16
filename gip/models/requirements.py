import cerberus
from gip.models import base


class Requirements(base.Model):

    def __init__(self, requirements):
        self.requirements = requirements
        super().__init__(
            scheme={
                'requirements': {
                    'type': 'list',
                    'schema': {
                        'type': 'dict',
                        'schema': {
                            'name': {
                                'type': 'string',
                                'required': True
                            },
                            'repo': {
                                'type': 'string',
                                'required': True
                            },
                            'type': {
                                'type': 'string',
                                'required': True,
                                'allowed': [
                                    'gitlab',
                                    'github'
                                ]
                            },
                            'version': {
                                'type': 'string'
                            },
                            'dest': {
                                'type': 'string'
                            }
                        }
                    }
                }
            }
        )

    def validate(self, requirements):
        """ Validate requirements against scheme

        :param requirements: List containing requirements
        :type list:

        :rtype: boolean
        """
        # Convert to dict since Cerberus only works with dicts
        requirements_dict = {
            'requirements': requirements
        }
        super().validate(requirements_dict)
