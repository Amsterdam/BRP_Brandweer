import datetime

import pytest

from requests.sessions import Session

from app import app as main_app
from config import config, check_env_vars, required_env_vars
from stuf.parse_0204 import _get_age, _get_age_category, _get_indicatoren
from stuf.stuf_0204 import get_Lv01


@pytest.fixture
def app():
    return main_app


def test_age():
    birthdate = datetime.date.today()
    assert _get_age(birthdate) == 0
    birthdate = datetime.date(day=birthdate.day, month=birthdate.month, year=birthdate.year - 1)
    assert _get_age(birthdate) == 1
    birthdate += datetime.timedelta(days=1)
    assert _get_age(birthdate) == 0


def test_age_categories():
    for i in [0, 11, 12]:
        assert _get_age_category(i) == "0-12"
    for i in [13, 69]:
        assert _get_age_category(i) == "13-69"
    for i in [70, 71]:
        assert _get_age_category(i) == "70+"
    for i in [-1, 999999]:
        assert _get_age_category(i) is None


def test_indicatoren():
    assert _get_indicatoren([]) == [{
        "aanvullende_informatie": "Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 0 pers., 70+ jaar: 0 pers.",
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        "waarschuwingsniveau": 3
    }]
    assert _get_indicatoren([13]) == [{
        "aanvullende_informatie": "Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 1 pers., 70+ jaar: 0 pers.",
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        "waarschuwingsniveau": 3
    }]
    assert _get_indicatoren([69]) == [{
        "aanvullende_informatie": "Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 1 pers., 70+ jaar: 0 pers.",
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        "waarschuwingsniveau": 3
    }]
    assert _get_indicatoren([13, 69]) == [{
        "aanvullende_informatie": "Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 2 pers., 70+ jaar: 0 pers.",
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        "waarschuwingsniveau": 3
    }]
    assert _get_indicatoren([12]) == [{
        "aanvullende_informatie": "Ingeschrevenen 0-12 jaar: 1 pers., 13-69 jaar: 0 pers., 70+ jaar: 0 pers.",
        "indicator": "Kwetsbare personen",
        "label": "Leeftijd",
        'waarschuwingsniveau': 2
    }]
    assert _get_indicatoren([70]) == [{
        'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 0 pers., 70+ jaar: 1 pers.',
        'indicator': 'Kwetsbare personen',
        'label': 'Leeftijd',
        'waarschuwingsniveau': 2
    }]
    assert _get_indicatoren([12, 70]) == [{
        'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 1 pers., 13-69 jaar: 0 pers., 70+ jaar: 1 pers.',
        'indicator': 'Kwetsbare personen',
        'label': 'Leeftijd',
        'waarschuwingsniveau': 2
    }]
    assert _get_indicatoren(range(9)) == [{
        'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 9 pers., 13-69 jaar: 0 pers., 70+ jaar: 0 pers.',
        'indicator': 'Kwetsbare personen',
        'label': 'Leeftijd',
        'waarschuwingsniveau': 2
    }]
    assert _get_indicatoren(range(10)) == [{
        'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 10 pers., 13-69 jaar: 0 pers., 70+ jaar: 0 pers.',
        'indicator': 'Kwetsbare personen',
        'label': 'Leeftijd',
        'waarschuwingsniveau': 2
    }, {
        'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 10 pers., 13-69 jaar: 0 pers., 70+ jaar: 0 pers.',
        'indicator': 'Aantal personen',
        'label': '10 ingeschrevenen',
        'waarschuwingsniveau': 2
    }]


# The following tests need mocked http responses
response_ok = b'<?xml version=\'1.0\' encoding=\'UTF-8\'?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><BG:synchroonAntwoordBericht xmlns:BG="http://www.egem.nl/StUF/sector/bg/0204" xmlns:StUF="http://www.egem.nl/StUF/StUF0204" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><StUF:stuurgegevens xmlns="http://www.egem.nl/StUF/StUF0204"><StUF:berichtsoort>La01</StUF:berichtsoort><StUF:entiteittype>ADR</StUF:entiteittype><StUF:sectormodel>BG</StUF:sectormodel><StUF:versieStUF>0204</StUF:versieStUF><StUF:versieSectormodel>0204</StUF:versieSectormodel><StUF:zender><StUF:organisatie>Amsterdam</StUF:organisatie><StUF:applicatie>CGM</StUF:applicatie></StUF:zender><StUF:ontvanger><StUF:applicatie>Meldkamer1</StUF:applicatie><StUF:gebruiker>meld-sys-user</StUF:gebruiker></StUF:ontvanger><StUF:referentienummer>MK0000008709</StUF:referentienummer><StUF:tijdstipBericht>2018013013011501</StUF:tijdstipBericht><StUF:antwoord><StUF:crossRefNummer>TGOLv01010</StUF:crossRefNummer></StUF:antwoord></StUF:stuurgegevens><BG:body xmlns="http://www.egem.nl/StUF/sector/bg/0204"><BG:ADR soortEntiteit="F" StUF:sleutelVerzendend="9072717152486" StUF:sleutelGegevensbeheer="9072717152486"><BG:postcode>1074ET</BG:postcode><BG:woonplaatsnaam xsi:nil="true" StUF:noValue="waardeOnbekend"/><BG:straatnaam>Rustenburgerstraat</BG:straatnaam><BG:huisnummer>14</BG:huisnummer><BG:huisletter>C</BG:huisletter><BG:huisnummertoevoeging xsi:nil="true" StUF:noValue="geenWaarde"/><BG:tijdvakGeldigheid><StUF:begindatumTijdvakGeldigheid xsi:nil="true" StUF:noValue="nietGeautoriseerd"/><StUF:einddatumTijdvakGeldigheid xsi:nil="true" StUF:noValue="nietGeautoriseerd"/></BG:tijdvakGeldigheid><BG:extraElementen><StUF:extraElement naam="identificatieAOA">0363200000399540</StUF:extraElement><StUF:extraElement naam="identificatieNummerAanduiding">0363200000399540</StUF:extraElement></BG:extraElementen><BG:ADRPRSVBL soortEntiteit="R" StUF:sleutelVerzendend="9072717290844" StUF:sleutelGegevensbeheer="9072717290844"><BG:tijdvakRelatie><StUF:begindatumRelatie>20010501</StUF:begindatumRelatie><StUF:einddatumRelatie xsi:nil="true" StUF:noValue="geenWaarde"/></BG:tijdvakRelatie><BG:PRS soortEntiteit="F" StUF:sleutelVerzendend="9072717290834" StUF:sleutelGegevensbeheer="9072717290834"><BG:geboortedatum>19620412</BG:geboortedatum><BG:datumOverlijden xsi:nil="true" StUF:noValue="geenWaarde"/><BG:tijdvakGeldigheid><StUF:begindatumTijdvakGeldigheid xsi:nil="true" StUF:noValue="nietGeautoriseerd"/><StUF:einddatumTijdvakGeldigheid xsi:nil="true" StUF:noValue="nietGeautoriseerd"/></BG:tijdvakGeldigheid></BG:PRS></BG:ADRPRSVBL></BG:ADR></BG:body></BG:synchroonAntwoordBericht></soapenv:Body></soapenv:Envelope>'  # noqa E501 line too long (2735 > 119 characters)
response_error = b'<?xml version=\'1.0\' encoding=\'UTF-8\'?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><BG:synchroonAntwoordBericht xmlns:BG="http://www.egem.nl/StUF/sector/bg/0204" xmlns:StUF="http://www.egem.nl/StUF/StUF0204" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><StUF:stuurgegevens xmlns="http://www.egem.nl/StUF/StUF0204"><StUF:berichtsoort>La01</StUF:berichtsoort><StUF:entiteittype>ADR</StUF:entiteittype><StUF:sectormodel>BG</StUF:sectormodel><StUF:versieStUF>0204</StUF:versieStUF><StUF:versieSectormodel>0204</StUF:versieSectormodel><StUF:zender><StUF:organisatie>Amsterdam</StUF:organisatie><StUF:applicatie>CGM</StUF:applicatie></StUF:zender><StUF:ontvanger><StUF:applicatie>Meldkamer1</StUF:applicatie><StUF:gebruiker>meld-sys-user</StUF:gebruiker></StUF:ontvanger><StUF:referentienummer>MK0000008711</StUF:referentienummer><StUF:tijdstipBericht>2018013013165699</StUF:tijdstipBericht><StUF:antwoord><StUF:crossRefNummer>TGOLv01010</StUF:crossRefNummer></StUF:antwoord></StUF:stuurgegevens><BG:body xmlns="http://www.egem.nl/StUF/sector/bg/0204"/></BG:synchroonAntwoordBericht></soapenv:Body></soapenv:Envelope>'  # noqa E501 line too long (1189 > 119 characters)


class MockResponse:
    content = None


def mockreturn(*args, **kwargs):
    return MockResponse()


def test_messages(monkeypatch):
    monkeypatch.setattr(Session, "request", mockreturn)

    MockResponse.content = response_ok
    msg = get_Lv01("0363200000399540", config)
    assert msg == [{
        'locatie': {
            'bag_id': '0363200000399540'
        },
        'indicatoren': [{
            'waarschuwingsniveau': 3,
            'indicator': 'Kwetsbare personen',
            'label': 'Leeftijd',
            'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 1 pers., 70+ jaar: 0 pers.'
        }]
    }]

    MockResponse.content = response_error
    msg = get_Lv01("0363200000399540x", config)
    assert msg == [{
        'locatie': {
            'bag_id': '0363200000399540x'
        },
        'error': 'Geen adres gevonden'
    }]


def test_http_responses(client, monkeypatch):
    monkeypatch.setattr(Session, "request", mockreturn)

    MockResponse.content = response_ok
    assert client.get('/brp_brandweer/0363200000399540').status_code == 200
    assert client.get('/brp_brandweer/0363200000399540').json == {
        'locatie': {
            'bag_id': '0363200000399540'
        },
        'indicatoren': [{
            'waarschuwingsniveau': 3,
            'indicator': 'Kwetsbare personen',
            'label': 'Leeftijd',
            'aanvullende_informatie': 'Ingeschrevenen 0-12 jaar: 0 pers., 13-69 jaar: 1 pers., 70+ jaar: 0 pers.'
        }]
    }
    MockResponse.content = response_error
    assert client.get('/brp_brandweer/0363200000399540x').status_code == 404


def test_swagger(client):
    assert client.get('/static/openapi.yaml').status_code == 200


def test_env_check(monkeypatch):
    for var in required_env_vars:
        monkeypatch.setenv(var, "any value")

    check_env_vars()

    for var in required_env_vars:
        monkeypatch.delenv(var)
        with pytest.raises(ValueError):
            check_env_vars()
        monkeypatch.setenv(var, "any other value")
        check_env_vars()
