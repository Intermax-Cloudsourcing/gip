import cerberus
from gip.models import base


class Lock(base.Model):

    def __init__(self):
        super().__init__(
            scheme={
                'lock': {
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

    def validate(self, locks):
        """ Validate locks against scheme

        :param data: List containing lockdata
        :type list:

        :rtype: boolean
        """
        # Convert to dict since Cerberus only works with dicts
        lock_dict = {
            'lock': locks
        }
        super().validate(lock_dict)
