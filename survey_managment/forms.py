from django import forms
from .models import Category
from .models import Question , Survey

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']   
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control '}),
        } 
    