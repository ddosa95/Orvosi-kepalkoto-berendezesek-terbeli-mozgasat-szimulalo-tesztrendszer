import requests
import unit_test_main as main

USER = 'tango-cs'
PASSWORD = 'tango'
HEADERS = {'content-type': 'application/json'}


def put_request(target_url, command, value=None):
    endpoint = f"{main.BASE_URL}{target_url}{command}"
    r = requests.put(endpoint, auth=(USER, PASSWORD), headers=HEADERS, data=value)
    if r.status_code == 200:
        print(r.text)

