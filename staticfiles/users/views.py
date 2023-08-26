import requests
from django.conf import settings
from django.shortcuts import render, redirect

from users.forms import CustomLoginForm


def client_validate_dni(request):
    if request.POST:       
        form = CustomLoginForm(request.POST)
        if form.is_valid(): 
            document_number = form.cleaned_data['document_number']
            url = f'{settings.REC_SERVER}/client_validate_dni/{document_number}/'        
            response = requests.get(url)    
            print(response.status_code )     
            if response.status_code == 200:
                return redirect('credit')       
        else:
            return render(request, "login.html", {'form': form})        
          
    return render(request, 'login.html')