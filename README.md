# BRP-Brandweer

API to provide the Brandweer with info about the ages of the habitants at a specific address

## Development

* Python 3.6

A VPN connection with datapunt is required to connect to BRP

The following variables need to be defined:

    export BRP_HOST="..."
    export BRP_CERT="..."
    export BRP_VERIFY="False"
    export BRP_ZENDER_APPLICATIE="..."
    export BRP_ZENDER_GEBRUIKER="..."
    export BRP_ONTVANGER_APPLICATIE="..."
    export BRP_ONTVANGER_ORGANISATIE="..."
    
The required information to set these variables can be found in the password management system under the key BRP_Brandweer.

## Status

The status of the project is 'Voorbereiding'.

The project in its current status only shows that the retrieval of the required information is technically possible.

In the next phase the project will have to be extended with an API and deployment scripts

### Run the tests

    python3 -m venv ~/venv/BRP_Brandweer
    source ~/venv/BRP_Brandweer/bin/activate
    
    cd src
    pip install -r requirements.txt
    
    cd brp_brandweer
    python config.py
    python parse_0204.py
    python stuf_0204.py
