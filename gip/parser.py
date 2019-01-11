import yaml
import cerberus

from gip import logger
from gip import models

LOG = logger.get_logger(__name__)


def validate_requirements(requirements):
    """ Validate requirements against scheme

    :param requirements: List containing requirements
    :type list:

    :rtype: boolean
    """
    # Convert to dict since Cerberus only works with dicts
    dict = {
        'requirements': requirements
    }
    scheme = models.requirements.get_validation_scheme()
    validator = cerberus.Validator(scheme)
    return validator.validate(dict)


def parse_requirements_file(path):
    """Parse requirements

    :param path: path to yamlfile
    :type path: pathlib.Path

    :rtype: object
    """
    try:
        file_stream = open(path, 'r')
    except OSError as e:
        LOG.exception(e)
    else:
        try:
            return yaml.safe_load(file_stream)
        except yaml.YAMLError as e:
            LOG.exception(e)
        finally:
            file_stream.close()
