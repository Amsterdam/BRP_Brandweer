"""

This module contains the global configuration

"""

import os

required_env_vars = [
    "BRP_HOST",
    "BRP_CERT",
    "BRP_VERIFY",
    "BRP_ZENDER_APPLICATIE",
    "BRP_ZENDER_GEBRUIKER",
    "BRP_ONTVANGER_APPLICATIE",
    "BRP_ONTVANGER_ORGANISATIE",
]


def get_var_value(var):
    """Retrieve the value of an environment variable

    Args:
        var (str): the name of the variable

    Returns:
        str: the value of the variable or None if undefined

    """
    return os.getenv(var)


config = {
    "cert": get_var_value("BRP_CERT"),
    "verify": False if get_var_value("BRP_VERIFY") == "False" else get_var_value("BRP_VERIFY"),
    "host": get_var_value("BRP_HOST"),
    "path": "/CGS/StUF/services/BGSynchroon/",
    "zender": {
        "applicatie": get_var_value("BRP_ZENDER_APPLICATIE"),
        "gebruiker": get_var_value("BRP_ZENDER_GEBRUIKER"),
    },
    "ontvanger": {
        "applicatie": get_var_value("BRP_ONTVANGER_APPLICATIE"),
        "organisatie": get_var_value("BRP_ONTVANGER_ORGANISATIE"),
    }
}


def check_env_vars():
    """Check for any missing required environment variables

    Returns:
        None

    Raises:
        ValueError: if any required environment variable is not defined

    """
    missing = [var for var in required_env_vars if get_var_value(var) is None]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
