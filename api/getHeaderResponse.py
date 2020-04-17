import requests
import json


def headerContent():
    headers = {'Content-Type': 'application/json'}
    return headers


def response(api_url):
    resp = requests.get(api_url, headers=headerContent())
    if resp.status_code == 200:
        data = json.loads(resp.content.decode())
        print('json response : ', data)
        return data
    else:
        print('didn\'t get any response from API ')
        return ''
