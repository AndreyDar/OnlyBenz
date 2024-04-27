import pycurl
from io import BytesIO

import json

requests_list = ['EQA-KLASSE','EQB-KLASSE', 'EQE-KLASSE', 'EQS-KLASSE', 'ESPRINTER', 'ECITAN', 'EQT', 'EVITO', 'EQV']

# Load the JSON configuration file
with open('../config/settings.json', 'r') as config_file:
    config = json.load(config_file)

def testCurl(classId):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://api.mercedes-benz.com/configurator/v2/markets/de_DE/models?classId=" + str(classId))
    c.setopt(c.HTTPHEADER, ['accept: application/json', 'x-api-key:' + config['API_Mercedes']['key']])
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    print(body.decode('utf-8'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for(classId) in requests_list:
        testCurl(classId)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
