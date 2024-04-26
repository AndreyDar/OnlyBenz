import pycurl
from io import BytesIO

import json

# Load the JSON configuration file
with open('config/settings.json', 'r') as config_file:
    config = json.load(config_file)

def testCurl():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://api.mercedes-benz.com/configurator/v2/markets/de_DE/models?bodyId=LIMOUSINE_LANG')
    c.setopt(c.HTTPHEADER, ['accept: application/json', 'x-api-key:' + config['API']['key']])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    print(body.decode('utf-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testCurl()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
