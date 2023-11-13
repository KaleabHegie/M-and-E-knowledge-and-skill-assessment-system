from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
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
    name = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    instruction = forms.CharField(min_length=5, widget=forms.TextInput(attrs={'class': 'form-control'}))
    start_at = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
    end_at = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control','type':'date'}))
   
    class Meta:
        model = Survey
        fields = ['name', 'instruction', 'start_at', 'end_at', 'survey_type' , 'for_line_ministry']
        widgets = {
            'survey_type': forms.Select(attrs={'class': 'form-control'}),
            'for_line_ministry': forms.SelectMultiple(attrs={'class': 'form-select select2'}),
        }

    def clean_start_at(self):
        start_at = self.cleaned_data.get('start_at')
        if start_at and start_at < timezone.now().date():
            raise forms.ValidationError('Start date must be after system date.')
        return start_at

    def clean_end_at(self):
        start_at = self.cleaned_data.get('start_at')
        end_at = self.cleaned_data.get('end_at')
        if start_at and end_at and end_at < start_at:
            raise forms.ValidationError('End date must be after start date.')
        return end_at
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['forsurvey', 'submitted_by']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answertext']


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
