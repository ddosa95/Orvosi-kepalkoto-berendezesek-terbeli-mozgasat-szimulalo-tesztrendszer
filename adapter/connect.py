import requests

API_BASE_URL = "http://192.168.1.72:9000"
ENDPOINT_PATH = "/tango/rest/rc4/hosts/tangobox-vm/10000/devices"
USER = 'tango-cs'
PASSWORD = 'tango'


def request(path):
    endpoint = f"{API_BASE_URL}{ENDPOINT_PATH}{path}"
    r = requests.get(endpoint, auth=(USER, PASSWORD))
    if r.status_code == 200:
        return r.text
