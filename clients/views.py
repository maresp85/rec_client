from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render

from app.utils import get_requests, post_requests


@login_required(login_url='/')
def get_credit(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    
    context = {}
    document_number = request.user.document_number
    device: str = ''
    try:
        os_system: str = request.user_agent.os.family  # returns 'iOS'        
        os_version: str = request.user_agent.os.version_string  # returns '5.1'
        os_device: str = request.user_agent.device.family  # returns 'iPhone'
        device = f'{os_device}-{os_system}-{os_version}'
    except:
        device = ''

    url = f'{settings.REC_SERVER}/credit_client/{document_number}?device={device}&ip_address={request.user.ip_address}'
    response = get_requests(url)
 
    if response.status_code == 200:        
        credit = response.json()
        context = {
            'credit': credit,
            'SERVER': settings.REC_SERVER,
        }
          
    return render(request, 'clients/credit.html', context)


def request_credit(request):
    if request.POST:
        url = f'{settings.REC_SERVER}/credit_request/'
        data: dict = {
            'mobile_number': request.POST['mobile_number'],
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'address': request.user.address,
        }
        
        if request.user.client_id:
            data.update({'client_id': request.user.client_id}) 
            data.update({'is_rec_client': True})
        else:
            data.update({'referred_code': request.user.referred_code})
      
        response = post_requests(url, data)
        if response.status_code == 200:
            messages.success(
                request, 
                'Solicitud de crédito enviada correctamente. Durante el transcurso del día será \n'
                'contactado por uno de nuestros asesores.'
            )

    return HttpResponseRedirect('/credito/')
