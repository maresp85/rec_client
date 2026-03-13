from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from social_django.models import UserSocialAuth

from app.utils import get_requests, post_requests
from app.email_utils import send_approval_code_email
from clients.models import ApprovalCodeEmailLog


@login_required(login_url='/')
def get_credit(request):
    if not request.user.email:
        google_login = UserSocialAuth.objects.filter(user=request.user).first()
        if google_login:
            user = request.user
            user.email = google_login.uid
            user.save(update_fields=['email'])

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
        email_sent = False

        # Enviar código de aprobación por correo para créditos pendientes
        if request.user.email:
            for item in credit:
                if item.get('status') == 50 and item.get('approval_code'):
                    credit_id = item.get('id')
                    already_sent = ApprovalCodeEmailLog.objects.filter(
                        user=request.user,
                        credit_id=credit_id,
                        success=True,
                    ).exists()

                    if not already_sent:
                        sent = send_approval_code_email(
                            user_email=request.user.email,
                            user_name=request.user.full_name or request.user.first_name,
                            approval_code=item['approval_code'],
                            credit_value=str(item.get('initial_balance', '')),
                        )
                        ApprovalCodeEmailLog.objects.create(
                            user=request.user,
                            credit_id=credit_id,
                            approval_code=item['approval_code'],
                            credit_value=str(item.get('initial_balance', '')),
                            email_to=request.user.email,
                            success=sent,
                        )
                        if sent:
                            email_sent = True
                    else:
                        email_sent = True

        context = {
            'credit': credit,
            'SERVER': settings.REC_SERVER,
            'email_sent': email_sent,
        }
          
    return render(request, 'clients/credit.html', context)


@login_required(login_url='/')
def request_credit(request):
    if request.POST:
        url = f'{settings.REC_SERVER}/credit_request/'
        data: dict = {
            'mobile_number': request.POST['mobile_number'],
            'document_number': request.user.document_number,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'address': request.user.address,
            'is_rec_client': False,
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
