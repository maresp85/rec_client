from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from app.utils import get_requests

from users.forms import CustomLoginForm, CreateUserForm, CustomReferralCodeForm
from users.models import Enterprise
from users.usecases import CreateUser


@csrf_exempt
def custom_login(request):
    if request.POST:       
        form = CustomLoginForm(request.POST)       
        
        if form.is_valid(): 
            document_number = form.cleaned_data['document_number']
            url = f'{settings.REC_SERVER}/validate_dni_digital_card/{document_number}/'        
            response = get_requests(url)

            if response.status_code == 200:
                data = response.json()

                if 'id' in data and data['id']:
                    company_data = data['office']       
                    create_company(company_data=company_data)

                    user = register_user(
                        form_data=response.json(), 
                        referred_code=data['referred_code'],
                        company_id=company_data['company'],
                    )
                            
                    if user:                        
                        login(request, user)
                        return HttpResponseRedirect('/credito/')                    
                else:
                    return HttpResponseRedirect('/codigo-referido/')                           
        else:         
            return render(request, 'users/login.html', { 'form': form })        
          
    return render(request, 'users/login.html')


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


def create_user_view(request, referred_code, company_id):     
    form = CreateUserForm()
    
    if request.POST:
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            user = register_user(
                form_data=form.cleaned_data, 
                referred_code=referred_code,
                company_id=company_id,
            )            

            if user:
                login(request, user)
                return HttpResponseRedirect('/credito/')   
        else:  
            return render(request, 'users/create_user.html', {'form': form})   

    return render(request, 'users/create_user.html', {'form': form})


def register_user(form_data, referred_code, company_id):
    usecase = CreateUser(
        data=form_data, 
        referred_code=referred_code,
        company_id=company_id,
    )
    usecase.execute()  
    document_number = form_data['document_number']

    return authenticate(username=document_number, password='secret*rec_client_2022')