from django.forms import ModelForm

from users.models import User
 

class CustomLoginForm(ModelForm):
    class Meta:        
        model = User  
        fields = ['document_number'] 

    def clean(self):
        super(CustomLoginForm, self).clean()
         
        document_number = self.cleaned_data.get('document_number')
        if not document_number or document_number == '':         
            self.add_error('document_number', 'El documento es requerido.')
     
        return self.cleaned_data