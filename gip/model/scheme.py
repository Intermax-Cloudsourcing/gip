import cerberus
from gip import exceptions

locks = {
    'dict': {
        'type': 'dict',
        'keyschema': {
            'type': 'string',
            'regex': '^[a-z-]+$'
        },
        'valueschema': {
            'type': 'string',
            'regex': '^[0-9a-z]+$'
        },
        'allow_unknown': True
    }
}

requirements = {
    'dict': {
        'type': 'list',
        'schema': {
            'type': 'dict',
            'schema': {
                'name': {
                    'type': 'string',
                    'regex': '^[a-z-]+$',
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


def validate(type, data):
    """
    TODO: Write doc
    """
    if type == 'locks':
        validator = cerberus.Validator(locks)
    elif type == 'requirements':
        validator = cerberus.Validator(requirements)

    # Add data to dict, Cerberus only works with dicts, not lists

    if validator.validate({'dict': data}):
        return True  # Valid data according to scheme
    else:
        raise exceptions.ValidationError(errors=validator.errors)
