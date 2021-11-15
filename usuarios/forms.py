from django.contrib.auth import forms
from django.forms import widgets

from .models import Usuario


class UserChangeForm(forms.UserChangeForm):
    
    #class Meta(forms.UserChangeForm.Meta):
    class Meta:    
        model = Usuario
        
        fields=(
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "licenca",
            "uf",
            "cidade",
            "sobre", 
            "image",)
        
class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = Usuario        