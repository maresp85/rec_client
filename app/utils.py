import requests
from django.conf import settings


def get_requests(url: str):
    return requests.get(
        url, 
        verify=False, 
        headers={'Authorization': f'token {settings.REC_TOKEN_SERVER}'}
    )


def post_requests(url: str, json: dict):
    return requests.post(
        url, 
        verify=False, 
        json=json,
        headers={'Authorization': f'token {settings.REC_TOKEN_SERVER}'}
    ) 