from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
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


class UserResponseFormA(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['age', 'department', 'line_ministry', 'year_of_experiance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
        self.fields['line_ministry'].widget.attrs.update({'class': 'form-control'})
        self.fields['year_of_experiance'].widget.attrs.update({'class': 'form-control'})



class AnonymousUserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['year_of_experiance' , 'department' , 'age'] 



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answertext']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['foranswer', 'document']


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AnalysisForm(forms.Form):
    survey_type = forms.ModelChoiceField(queryset=SurveyType.objects.all(),
                                  widget=forms.Select(attrs={"hx-get":"load_survey/","hx-target":"#id_survey" ,'class': ' form-control'}))
    survey = forms.ModelChoiceField(queryset=Survey.objects.none(),
                                     widget=forms.Select(attrs={"hx-get":"load_ministry/","hx-target":"#id_line_ministry" , 'class': 'form-control'}))
    line_ministry = forms.ModelChoiceField(
        queryset=Line_ministry.objects.none(),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    

    