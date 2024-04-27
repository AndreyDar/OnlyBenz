import pycurl
from io import BytesIO

import json

requests_list = ['EQA-KLASSE']
#requests_list = ['EQA-KLASSE','EQB-KLASSE', 'EQE-KLASSE', 'EQS-KLASSE', 'ESPRINTER', 'ECITAN', 'EQT', 'EVITO', 'EQV']

# Load the JSON configuration file
with open('../config/settings.json', 'r') as config_file:
    config = json.load(config_file)

def testCurl(classId):
    buffer = BytesIO()
    c = pycurl.Curl()
    #c.setopt(c.URL, "https://api.mercedes-benz.com/configurator/v2/markets/de_DE/models/2437011/configurations/initial")
    c.setopt(c.URL, "https://api.mercedes-benz.com/configurator/v2/markets/de_DE/models/2437011/configurations/AU-311_LE-L_LU-696_MJ-805_PC-904-P59-PBG-PSA-U59-U62_PS-953%23-B05%23-E01%23_SA-01U-02B-13U-20U-218-243-258-261-270-286-287-294-310-345-351-355-362-365-367-39U-400-428-475-504-51U-521-537-543-55H-580-5B0-608-632-63B-677-70B-725-72B-73B-79B-7U2-82B-83B-859-873-877-88B-890-942-969-986-9B2-B13-B51-B53-B59-L3E-R05-R31-U01-U10-U12-U22-U35-U55-U60_SC-0S3-0U1-1B3-2U1-2U8-502-51B-5V4-6P5-7B4-7S3-7S8-8P3-8S8-8U6-8U8-998-9U8-BAE-EMD-K13-K37-K45-R7H/selectables")
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
