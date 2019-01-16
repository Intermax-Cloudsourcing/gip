import yaml
import cerberus
import sys
import os

from gip import logger
from gip import exceptions
from gip import models

LOG = logger.get_logger(__name__)


def read_yaml(path):
    """Parse YAML file to Python object

    :param path: path to yamlfile
    :type path: pathlib.Path

    :rtype: dict
    """
    # TODO: Rewrite to with open
    try:
        file_stream = open(path, 'r')
    except OSError as e:
        LOG.exception(e)
    else:
        try:
            return yaml.safe_load(file_stream)
        except yaml.YAMLError as e:
            raise exceptions.ParserError(e)
        finally:
            file_stream.close()


def write_yaml(path, data):
    """Write Python object to YAML

    :param path: path to yamlfile
    :type path: pathlib.Path

    :rtype: None
    """
    # TODO: Rewrite to with open
    try:
        file_stream = open(path, 'w')
    except OSError as e:
        LOG.exception(e)
    else:
        try:
            yaml.safe_dump(
                data,
                stream=file_stream,
                default_flow_style=False
            )
        except yaml.YAMLError as e:
            raise exceptions.ParserError(e)
        finally:
            file_stream.close()


def sysexit(code=1):
    sys.exit(code)


def sysexit_with_message(msg, code=1):
    LOG.critical(msg)
    sysexit(code)


def remove_file(path):
    """
    Remove file from disk
    """
    #TODO: fix some exception handling
    os.remove(path)
