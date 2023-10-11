from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


from .models import *
# Create your views here.

def indexView (request):
    return render(request, 'index.html', {})

def surveyCreationView (request):
    return render(request, 'surveyCreation.html', {})


def Mychartanalysis(request):
    data={}
    return render(request,'chart_analysis.html',data)

def questionnaireView(request):
    return render(request, 'questionnaires.html')

def questionnaireDetailView(request):
    return render(request, 'questionnaireDetail.html')

def survey(request):
    return render(request, 'survey.html')

def chooseSurvey(request):
    return render(request, 'chooseSurvey.html')

def displayQuestion(request):
    return render(request, 'displayQuesion.html')

def createForm(request):
    k = Question.objects.all()
    print(k)
    context = {'questions' : k  }
    return render(request, 'createForm.html', context)

def createFormTWO(request, zform):
    context = {'zform':zform}
    return render(request, 'createForm.html', context)


def questionCreationByType(request):
    if request.method == 'POST':
        QuestionTitle = request.POST.get('QuestionTitle')
        QuestionType = 'text'
        ForQuestionnaire = Questionnaire.objects.get(name="M&E") 
        question = Question.objects.create(title=QuestionTitle, question_type=QuestionType, for_questionnaire=ForQuestionnaire,has_weight=True, allow_doc=True ,weight=3)
        question.save()
        return redirect("survey_managment:createForm")
    else: 
        return HttpResponse('sorry')
        
