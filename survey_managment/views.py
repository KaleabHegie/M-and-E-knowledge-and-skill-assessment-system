from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


from .models import *


# Create your views here.



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed Succesussfuly')
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'survey_managment/change_password.html', {'form': form})

from django.shortcuts import render, get_object_or_404

def indexView(request):
    survey_id = request.GET.get('survey_id')
    if survey_id:
        survey = get_object_or_404(Survey, id=survey_id)
        questionnaires = survey.questionnaire_set.all()
        context = {
            'survey': survey,
            'questionnaires': questionnaires,
        }
        return render(request, 'index.html', context)
    else:
        surveys = Survey.objects.all()
        return render(request, 'index.html', {'surveys': surveys})

# def loginView(request):
#     return render(request, 'login.html')

def forgotPasswordView(request):
    return render(request, 'forgot-password.html')

def surveyCreationView (request):
    return render(request, 'surveyCreation.html', {})

def user_profile(request):
    return render(request , 'profile.html' )

def edit_profile(request):
    return render(request , 'edit_profile.html' )

def users(request):
    return render(request , 'user.html' )



def change_password(request):
    return render(request , 'password_change.html' )
# def user_registration(request):
#     return render(request , 'userRegistration.html' )

def Mychartanalysis(request):
    data={}
    return render(request,'chart_analysis.html',data)

def surveyQuestionnaireView(request, id):
    data = {
        'id':id,
        'questionnaires':  Questionnaire.objects.all(),
    }
    return render(request, 'surveyQuestionnaire.html', data)

def surveyQuestionnaireDetailView(request, survey_id, questionnaire_id):
    questions = Question.objects.filter(for_questionnaire = questionnaire_id)

    data = {
        'questions': questions,
    }
    return render(request, 'surveyQuestionnaireDetail.html', data)

def surveyQuestionnaireView(request, id):
    data = {
        'id':id,
        'questionnaires':  Questionnaire.objects.all(),
    }
    return render(request, 'surveyQuestionnaire.html', data)

def surveyQuestionnaireDetailView(request, survey_id, questionnaire_id):
    questions = Question.objects.filter(for_questionnaire = questionnaire_id)

    data = {
        'questions': questions,
    }
    return render(request, 'surveyQuestionnaireDetail.html', data)

def questionnaireView(request):
    return render(request, 'questionnaires.html')

def questionnaireDetailView(request):
    return render(request, 'questionnaireDetail.html')


def survey(request):
    data = {
        'surveys': Survey.objects.all(),
        }
    return render(request, 'survey.html', data)

    data = {
        'surveys': Survey.objects.all(),
        }
    return render(request, 'survey.html', data)


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
    






#######  Skill Assessment Survey View #####

def skill_assessment_survey_view(request):
    Question_list = Question.objects.all()
    Catagory_list = Catagory.objects.all()
    context ={
      'Question_list':Question_list ,'Catagory_list':Catagory_list
    }
    return render(request,'SkillAssessmentSurvey.html',context)

