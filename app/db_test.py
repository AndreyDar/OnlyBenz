from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.exceptions import APIException
from recombee_api_client.api_requests import *
import random
import json

with open('../config/settings.json', 'r') as config_file:
    config = json.load(config_file)


client = RecombeeClient(config['recombee']['db_id'], config['recombee']['db_private_token'], region=Region.EU_WEST)

client.send(SetItemValues('xyz',
    {
        "modelId": "4656001",
        "name": "G 580 mit EQ Technologie",
        "shortName": "G 580 mit EQ Technologie",
        "typeClass": "N465"
    },
    cascade_create=True
))
