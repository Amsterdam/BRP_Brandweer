"""

This module contains the logic to send and receive Stuf messages

"""

import requests
import datetime

from requests import RequestException
import xml.etree.ElementTree as ET

from .config_0204 import ns, soap_action
from .parse_0204 import parse_message

def _get_Lv01_message(bag_id, zender, ontvanger):
    """Get the stuf message Lv01

    Args:
        bag_id (str): the BAG id for which the message should be constructed
        zender (dict): The sender details
        ontvanger (dict): The receiver details

    Returns:
        str: the stuf message

    """
    tijdstip_bericht = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    namespaces = " ".join([f'xmlns:{key}="{value}"' for key, value in ns.items()])
    return f"""
    <soapenv:Envelope {namespaces}>
       <soapenv:Header/>
       <soapenv:Body>
          <ns:vraagBericht>
             <stuf:stuurgegevens>
                <stuf:berichtsoort>Lv01</stuf:berichtsoort>
                <stuf:entiteittype>ADR</stuf:entiteittype>
                <stuf:sectormodel>BG</stuf:sectormodel>
                <stuf:versieStUF>0204</stuf:versieStUF>
                <stuf:versieSectormodel>0204</stuf:versieSectormodel>
                <stuf:zender>
                   <stuf:applicatie>{zender["applicatie"]}</stuf:applicatie>
                   <stuf:gebruiker>{zender["gebruiker"]}</stuf:gebruiker>
                </stuf:zender>
                <stuf:ontvanger>
                   <stuf:organisatie>{ontvanger["organisatie"]}</stuf:organisatie>
                   <stuf:applicatie>{ontvanger["applicatie"]}</stuf:applicatie>
                </stuf:ontvanger>
                <stuf:referentienummer>TGOLv01010</stuf:referentienummer>
                <stuf:tijdstipBericht>{tijdstip_bericht}</stuf:tijdstipBericht>
                <stuf:vraag>
                   <stuf:sortering>01</stuf:sortering>
                   <stuf:maximumAantal>15</stuf:maximumAantal>
                </stuf:vraag>
             </stuf:stuurgegevens>
             <ns:body>
                <ns:ADR soortEntiteit="F">
                   <identificatieNummerAanduiding>{bag_id}</identificatieNummerAanduiding>
                </ns:ADR>
                <ns:ADR soortEntiteit="F">
                   <identificatieNummerAanduiding>{bag_id}</identificatieNummerAanduiding>
                </ns:ADR>
                <ns:ADR soortEntiteit="F">
                   <postcode stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <woonplaatsnaam stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <straatnaam stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <huisnummer stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <huisletter stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <huisnummertoevoeging stuf:noValue="geenWaarde" xsi:nil="true"/>
                   <identificatieNummerAanduiding stuf:noValue="geenWaarde" xsi:nil="true"/>
                 <ADRPRSVBL soortEntiteit="R">
                     <PRS soortEntiteit="F">
                         <geboortedatum StUF:noValue="geenWaarde" xsi:nil="true"/>
                         <datumOverlijden StUF:noValue="geenWaarde" xsi:nil="true"/>
                      </PRS>
                   </ADRPRSVBL>
                   </ns:ADR>
             </ns:body>
          </ns:vraagBericht>
       </soapenv:Body>
    </soapenv:Envelope>
    """


def get_Lv01(bag_ids, config):
    """Get the Lv01 message

    Args:
        bag_ids (list(str)): any list of BAG ids
        config (dict): the configuratin to use for requesting the message

    Returns:
        list(dict): a list of address informations for the BAG ids

    """
    session = requests.Session()

    session.cert = config["cert"]
    session.verify = config["verify"]

    url = config["host"] + config["path"]

    if isinstance(bag_ids, str):
        # Accept string arguments, automatically convert to list
        bag_ids = [bag_ids]

    results = []
    for bag_id in bag_ids:
        data = _get_Lv01_message(
            bag_id=bag_id,
            zender=config["zender"],
            ontvanger=config["ontvanger"]
        )

        headers = {
            "Content-Type": "text/xml;charset=UTF-8",
            "SOAPAction": soap_action,
            "Content-Length": str(len(data)),
        }

        error_message = None
        try:
            request = session.post(
                url=url,
                data=data,
                headers=headers
            )

            xml = ET.fromstring(request.content)
            addresses = xml.findall(".//ns:ADR", ns)
            if not addresses:
                error_message = f"Geen adres gevonden"
        except ET.ParseError as err:
            error_message = f"Bericht kan niet worden vertaald"
        except RequestException as err:
            error_message = f"Bericht kan niet worden opgehaald"

        if error_message:
            results.append(parse_message(bag_id, None, error_message=error_message))
        else:
            results.extend([parse_message(bag_id, adres) for adres in addresses])

    return results
