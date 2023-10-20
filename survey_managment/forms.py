from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Category
from .models import *

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']   
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control '}),
        } 
    



class SurveyForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise ValidationError("Name must be at least 5 characters long.")
        return name

    def clean_start_at(self):
        start_at = self.cleaned_data['start_at']
        if start_at <= timezone.now().date():
            raise ValidationError("Start date must be in the future.")
        return start_at

    def clean_end_at(self):
        end_at = self.cleaned_data['end_at']
        start_at = self.cleaned_data.get('start_at')
        if start_at and end_at <= start_at:
            raise ValidationError("End date must be after the start date.")
        return end_at

    class Meta:
        model = Survey
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'survey_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Survey Name',
            'start_at': 'Start Date',
            'end_at': 'End Date',
            'survey_type': 'Survey Type',
        }

        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


