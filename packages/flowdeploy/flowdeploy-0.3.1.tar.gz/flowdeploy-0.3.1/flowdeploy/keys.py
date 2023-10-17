import os
from loguru import logger

from flowdeploy.exceptions import FlowDeployKeyError


def print_set_key_instructions(cli):
    logger.error("Key not found. Please set the FLOWDEPLOY_KEY environment variable to your api key.")
    logger.error("Function call:")
    if cli:
        logger.error("    flowdeploy set-key YOUR_KEY_HERE")
    else:
        logger.error("    flowdeploy.set_key(YOUR_KEY_HERE)")


def get_key(cli):
    """Retrieves the FlowDeploy API key, if it is set."""
    try:
        key = os.environ.get("FLOWDEPLOY_KEY", os.environ.get("TOOLCHEST_KEY"))
        if not key:
            print_set_key_instructions(cli)
            raise FlowDeployKeyError()
    except KeyError as e:
        print_set_key_instructions(cli)
        return e
    return key


def set_key(key):
    """Sets the FlowDeploy auth key (env var FLOWDEPLOY_KEY) to the given value.

    :param key: key value (str) or path to file containing key. If given a filename,
        the file must consist of only the key itself.

    Usage::

        >>> import flowdeploy
        >>> flowdeploy.set_key(YOUR_KEY_HERE)

    """

    if os.path.isfile(key):
        with open(key, "r") as f:
            os.environ["FLOWDEPLOY_KEY"] = f.read().strip()
    else:
        os.environ["FLOWDEPLOY_KEY"] = key
