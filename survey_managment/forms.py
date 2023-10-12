from django import forms
from .models import Question

class QuestionForm(forms.Form):
    class Meta:
        model = Question
        fields = "__all__"    
    