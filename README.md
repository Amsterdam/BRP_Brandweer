# BRP-Brandweer

API to provide the Brandweer with indicators about the number and ages of the habitants at a specific address

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

### Configuration

    python3 -m venv ~/venv/BRP_Brandweer
    source ~/venv/BRP_Brandweer/bin/activate
    
    cd src
    pip install -r requirements.txt

### Run the tests

    cd brp_brandweer/api
    flake8
    python -m pytest

### Run the server locally

    cd brp_brandweer/api
    python app.py
