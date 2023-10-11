from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.forms import PasswordChangeForm

     

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
