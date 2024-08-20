from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.utils import get_requests

from users.forms import CustomLoginForm, CreateUserForm, CustomReferralCodeForm
from users.models import Enterprise, User
from users.usecases import CreateUser


@csrf_exempt
def email_login(request): 
          
    return render(request, 'users/email_login.html')


@csrf_exempt
def custom_login(request):
    if request.POST:       
        form = CustomLoginForm(request.POST)       
        
        if form.is_valid(): 
            document_number = form.cleaned_data['document_number']

            user = User.objects.filter(document_number=document_number).first()

            if user:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                if not user.email:
                    return HttpResponseRedirect('/email-login/')
                
                return HttpResponseRedirect('/credito/')
            
            url = f'{settings.REC_SERVER}/validate_dni_digital_card/{document_number}/'        
            response = get_requests(url)
            
            if response.status_code == 200:
                data = response.json()                

                if 'document_number' in data and data['document_number']:
                    company_data = data['office']
                    create_company(company_data=company_data)
                 
                    if not user:
                        user = register_user(
                            form_data=response.json(),
                            referred_code=data['referred_code'],
                            company_id=company_data['company'],
                            office_name=company_data['name'],
                            office_phone_number=company_data.get('phone_number'),
                            ip_address=request.POST['ip_address'] if request.POST.get('ip_address') else '',
                        )                        

                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                        if not user.email:
                            return HttpResponseRedirect('/email-login/')
               
                        return HttpResponseRedirect('/credito/')
                
                else:
                    return HttpResponseRedirect('/codigo-referido/')  
                                             
        else:            
            return render(request, 'users/custom_login.html', { 'form': form })        
    
    return render(request, 'users/custom_login.html')


def reffered_code_view(request):
    if request.POST:       
        form = CustomReferralCodeForm(request.POST)       
        
        if form.is_valid(): 
            referred_code = form.cleaned_data['referred_code']
            url = f'{settings.REC_SERVER}/validate_referred_code_digital_card/{referred_code}/'        
            response = get_requests(url)
          
            if response.status_code == 200:
                data = response.json()

                if 'id' in data and data['id']:                 
                    company_data = data['office']
                    create_company(company_data=company_data)

                    url = reverse(
                        'create_user', 
                        kwargs={
                            'referred_code': referred_code,
                            'company_id': company_data['company'],
                            'office_name': company_data['name'],
                            'office_phone_number': company_data.get('phone_number'),
                        }
                    )
                    return HttpResponseRedirect(url)
            
            form.add_error('referred_code', 'El código de referido no existe')
          
        return render(request, 'users/referral_code.html', { 'form': form })        
          
    return render(request, 'users/referral_code.html')


def create_company(company_data):
    company = Enterprise.objects.filter(name=company_data['company_name']).first()
    
    mobile_phone = None
    if 'company_phone_number' in company_data:
        mobile_phone = company_data['company_phone_number']

    if not company:
        Enterprise.objects.create(
            id=company_data['company'],
            name=company_data['company_name'],
            mobile_phone=mobile_phone,
        )
    else:        
        company.mobile_phone = mobile_phone
        company.save(update_fields=['mobile_phone'])


def create_user_view(
    request, 
    referred_code: str, 
    company_id: int, 
    office_name: str = '', 
    office_phone_number: str = ''
):     
    form = CreateUserForm()
    
    if request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            user = register_user(
                form_data=form.cleaned_data,
                referred_code=referred_code,
                company_id=company_id,
                office_name=office_name,
                office_phone_number=office_phone_number,
                ip_address=request.POST['ip_address'] if request.POST.get('ip_address') else '',
            )

            if user:
                login(request, user)
                return HttpResponseRedirect('/email-login/')
        else:  
            return render(request, 'users/create_user.html', {'form': form})   

    return render(request, 'users/create_user.html', {'form': form})


def register_user(
    form_data: dict,
    referred_code: str,
    company_id: int,
    office_name: str = '',
    office_phone_number: str = '',
    ip_address: str = ''
):
    usecase = CreateUser(
        data=form_data, 
        referred_code=referred_code,
        company_id=company_id,
        office_name=office_name,
        office_phone_number=office_phone_number,
        ip_address=ip_address,
    )
    usecase.execute()

    document_number = form_data['document_number']

    return authenticate(username=document_number, password='secret*rec_client_2022')
