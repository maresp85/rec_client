from django import forms
from django.forms import ModelForm

from users.models import User, City
 

class CustomLoginForm(forms.Form):
    document_number = forms.CharField(max_length=26)

    def clean(self):
        super(CustomLoginForm, self).clean()
         
        document_number = self.cleaned_data.get('document_number')
        if not document_number or document_number == '':         
            self.add_error('document_number', 'El documento es requerido.')
     
        return self.cleaned_data
    

class CustomReferralCodeForm(forms.Form):
    referred_code = forms.CharField(max_length=26)

    def clean(self):
        super(CustomReferralCodeForm, self).clean()
         
        referred_code = self.cleaned_data.get('referred_code')
        if not referred_code or referred_code == '':         
            self.add_error('referred_code', 'El código del referido es requerido.')
     
        return self.cleaned_data


class CreateUserForm(ModelForm):
    city = forms.ModelChoiceField(label='ciudad', queryset=City.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.filter(is_active=True)

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'address', 
            'address_payment',
            'mobile_number',
            'document_number',
            'city',
        ]

    def clean(self):
        super(CreateUserForm, self).clean()         
        document_number = self.cleaned_data.get('document_number')
        user = User.objects.filter(document_number=document_number).first()
        if user:         
            self.add_error('document_number', 'El número de documento ya existe.')
     
        return self.cleaned_data