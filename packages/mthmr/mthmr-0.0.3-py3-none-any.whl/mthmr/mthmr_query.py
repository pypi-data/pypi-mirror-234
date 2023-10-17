import requests

def get_customers(URL, Token):
    headers = {
        'accept': 'application/json',
        'Authorisation': 'Bearer '+Token,
    }
    response = requests.get(URL+'customers', headers=headers)
    return response.text


def add_customers(URL, Token, payload):
    headers = {
        'accept': 'application/json',
        'Authorisation': 'Bearer '+Token,
    }
    response = requests.post(URL+'customers/', headers=headers, json=payload)
    return response.text


def add_transactions(URL, Token, payload):
    headers = {
        'accept': 'application/json',
        'Authorisation': 'Bearer '+Token,
    }
    response = requests.post(URL+'transactions/', headers=headers, json=payload)
    return response.text