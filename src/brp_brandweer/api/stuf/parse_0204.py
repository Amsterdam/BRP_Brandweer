"""

This module contains the logic to parse the Stuf messages and retrieve the required information for the Brandweer

The specs are as follows:

Indien: 1 of meer personen 12 jaar of jonger
        en/of 1 of meer personen 70 jaar of ouder
Waarschuwingsniveau: 2
Indicator: Kwetsbare personen
Label: Leeftijd
Aanvullende_informatie: Ingeschrevenen 0 - 12 jaar: x pers., 13-69 jaar: y pers., 70+ jaar: z pers.

Alle overige gevallen
Waarschuwingsniveau: 3
Indicator: Kwetsbare personen
Label: Leeftijd
Aanvullende_informatie: Ingeschrevenen 0 - 12 jaar: x pers., 13-69 jaar: y pers., 70+ jaar: z pers.

Aanvullend is er nog een tweede indicator mogelijk
Die wordt alleen toegevoegd indien er in totaal 10 of meer personen staan ingeschreven
Waarbij XYZ het totaal aantal ingeschrevenen is:

Indien: 10 of meer personen
Waarschuwingsniveau : 2
Indicator: Aantal personen
Label: XYZ Ingeschrevenen
Aanvullende_informatie
Ingeschrevenen 0 - 12 jaar: x pers., 13-69 jaar: y pers., 70+ jaar: z pers.

De eerste indicator is er dus altijd (waarschuwingsniveau 2 of 3) als de BRP iets teruggeeft, het tweede niet altijd.

"""

import datetime
from dateutil.relativedelta import relativedelta

import xml.etree.ElementTree as ET

from .config_0204 import ns

_age_categories = [
    {
        "name": '0-12',
        "min_age": 0,
        "max_age": 12
    },
    {
        "name": '13-69',
        "min_age": 13,
        "max_age": 69
    },
    {
        "name": '70+',
        "min_age": 70,
        "max_age": 125
    }
]

# indicatoren parameters
_kwetsbare_categories = [_age_categories[i]["name"] for i in [0, 2]]    # 0-12 and 70+
_kritisch_aantal_personen = 10                                          # additional indicator requested


def _get_age(birthdate):
    """Get the age giving a birthdate

    Args:
        birthdate (datetime.date): the birthdate

    Returns:
        int: the corresponding age at the current date

    """
    now = datetime.datetime.now().date()
    return relativedelta(now, birthdate).years


def _get_age_category_names():
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
    matches = [c for i, c in enumerate(_age_categories) if c["min_age"] <= age <= c["max_age"]]
    return matches[0]["name"] if matches else None


def _get_indicatoren(ages):
    """Get the indicatoren (kwetsbaarheid en aantal) for the given ages

    Args:
        ages (list): A list of ages of persons

    Returns:
        list(dict): a list of indicator objects that correspond to the given list of ages

    """
    aantal_personen = len(ages)

    # Initialize each age category and then increment for each age in the respective category
    age_categories = {category: 0 for category in _get_age_category_names()}
    for category in [_get_age_category(age) for age in ages]:
        age_categories[category] += 1

    # compose a string that describes the number of persons per age category
    aanvullende_informatie = "Ingeschrevenen " + \
                             ', '.join([f"{category} jaar: {age_categories[category]} pers."
                                        for category in _get_age_category_names()])

    # Convert the ages into indicatoren
    indicatoren = [{
        "waarschuwingsniveau": 2 if sum([age_categories[category] for category in _kwetsbare_categories]) else 3,
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        "aanvullende_informatie": aanvullende_informatie
    }]

    if aantal_personen >= _kritisch_aantal_personen:
        indicatoren.append({
            "waarschuwingsniveau": 2,
            "indicator": "Aantal personen",
            "label": f"{aantal_personen} ingeschrevenen",
            "aanvullende_informatie": aanvullende_informatie
        })

    return indicatoren


def parse_message(bag_id, address, error_message=None):
    """Parse the stuf address message into a response object for the brandweer

    Args:
        bag_id (str): the BAG id that corresponds with the message
        address (xml.etree.ElementTree): the address part of the stuf message
        error_message (str): any error message that relates to the retrieval of the stuf message

    Returns:
        dict: the parsed message, contains an error property in case of any errors

    """
    # Register the bag_id for this address
    info = {
        "locatie": {
            "bag_id": bag_id,
        },
    }

    if error_message:
        info["error"] = error_message
        return info

    # No errors so far, parse the message

    # try to get the ages of all persons (PRS) that live at the address
    try:
        ages = [
            _get_age(birthdate)
            for birthdate
            in [
                datetime.datetime.strptime(prs.find("./ns:geboortedatum", ns).text, "%Y%m%d").date()
                for prs in address.findall(".//ns:PRS", ns)
                if not prs.find("./ns:datumOverlijden", ns).text
            ]
        ]
    except ValueError:
        info["error"] = "Bericht kan niet worden vertaald"
        return info

    info["indicatoren"] = _get_indicatoren(ages=ages)
    return info
