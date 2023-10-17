from django import forms
from .models import Category
from .models import Question , Survey , Questionnaire

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']   
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control '}),
        } 
    
class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name', 'year']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.DateInput(attrs={'class': 'form-control'}),
        }    

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ['name', 'instruction']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'instruction': forms.Textarea(attrs={'class': 'form-control'}),
        }
        