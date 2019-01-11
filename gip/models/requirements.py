from gip.models import base

scheme = ""


def get_validation_scheme():
    return {
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
