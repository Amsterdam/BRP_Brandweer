"""

This module contains the logic to parse the Stuf messages and retrieve the required information for the Brandweer


"""

import datetime
from dateutil.relativedelta import relativedelta

import xml.etree.ElementTree as ET

from config import check_env_vars
from config_0204 import ns

_age_categories = [
    {
        "name": '<=12',
        "max_age": 12
    },
    {
        "name": '12-75',
        "max_age": 75
    },
    {
        "name": '75+',
        "max_age": 999
    }
]

def _get_age(birthdate):
    """Get the age giving a birthdate

    Args:
        birthdate (datetime.date): the birthdate

    Returns:
        int: the corresponding age at the current date

    """
    now = datetime.datetime.now().date()
    return relativedelta(now, birthdate).years


def _get_age_categories():
    """Get the age categories

    Returns:
        list(str): the names of the age categories

    """
    return [category["name"] for category in _age_categories]


def _get_age_category(age):
    """Get the age category for a given age

    Args:
        age (int): the age

    Returns:
        str: the name of the age category for the given age

    """
    matches = [c for i, c in enumerate(_age_categories) if age <= c["max_age"]]
    category = matches[0] if matches else len(_age_categories)
    return category["name"]


def parse_message(bag_id, address, error_message=None):
    """Parse the stuf address message into a dictionary

    Args:
        bag_id (str): the BAG id that corresponds with the message
        address (xml.etree.ElementTree): the address part of the stuf message
        error_message (str): any error message that relates to the retrieval of the stuf message

    Returns:
        dict: the parsed message

    """
    # Register the bag_id for this address
    info = {
        "bag_id": bag_id,
        "error": error_message
    }

    if not error_message:
        # only parse the message if there are no errors

        # get basic adres information
        for prop in ["straatnaam", "huisnummer", "huisletter", "huisnummertoevoeging"]:
            child = address.find(f"./ns:{prop}", ns)
            info[prop] = child.text if isinstance(child, ET.Element) else None

        # and the ages of all persons (PRS) that live at that address
        ages = [
            _get_age(birthdate)
            for birthdate
            in [
                datetime.datetime.strptime(prs.find("./ns:geboortedatum", ns).text, "%Y%m%d").date()
                for prs in address.findall(".//ns:PRS", ns)
                if not prs.find("./ns:datumOverlijden", ns).text
            ]
        ]

        # Initialize each age category and then increment for each age in the respective category
        for category in _get_age_categories():
            info[category] = 0

        for category in [_get_age_category(age) for age in ages]:
            info[category] += 1

    return info


if __name__ == "__main__":
    # execute only if run as a script
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    check_env_vars()

    birthdate = datetime.date(1962, 1, 17)
    pp.pprint(_get_age(birthdate))
    pp.pprint(_get_age_category(_get_age(birthdate)))
    for i in [11, 12, 13, 74, 75, 76]:
        print(i, _get_age_category(i))
