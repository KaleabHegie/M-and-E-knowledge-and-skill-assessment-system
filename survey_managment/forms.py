from django import forms
from .models import Question , Survey

class QuestionForm(forms.Form):
    class Meta:
        model = Question
        fields = "__all__"    

class QuestionCreateByEdit(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

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
        fields = ['title']
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control'})
        }
    