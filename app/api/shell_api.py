import pycurl
import json

from io import BytesIO

def call_shell_api_with_curl():
    try:
        with open('config/settings.json', 'r') as config_file:
            config = json.load(config_file)

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, 'https://api.mercedes-benz.com/configurator/v2/markets/de_DE/models?bodyId=LIMOUSINE_LANG')
        c.setopt(c.HTTPHEADER, ['accept: application/json', 'x-api-key:' + config['API']['key']])
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        return json.loads(buffer.getvalue())
    except pycurl.error as e:
        return {"error": "Shell command failed", "details": str(e)}