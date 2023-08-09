import requests
from django.conf import settings
from django.shortcuts import render


def get_credit(request):
    url = f'{settings.REC_SERVER}/credit_client/655/'
    response = requests.get(url)
    context = {}
    if response.status_code == 200:
        context = {
            'data': response.json()
        }
          
    return render(request, 'credit.html', context)