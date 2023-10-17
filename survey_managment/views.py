from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from datetime import datetime
from .forms import CategoryForm


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

   

def newForm(request):
    if request.method == 'POST':
        # new Questionnaire
        name = request.POST.get('Title')
        instruction = request.POST.get('Instruction')
        created_at = datetime.now()
        # survey = ??
        newQuestionnaire = Questionnaire.objects.create(name=name, instruction=instruction, created_at=created_at)
        newQuestionnaire.save()
        request.session['questionnaire_id'] = newQuestionnaire.id 
       
        # new categories
        category = request.POST.getlist('category')
        print(category)
        for i in category:
            name = i
            Category.objects.create(name=name)


        return redirect('survey_managment:questionCreationByType' )
    else :
         cateForm = CategoryForm()
         return render(request, 'createForm.html', {'cateForm' : cateForm})

def questionCreationByType(request):
    category = Category.objects.all()
    if request.method == 'POST':
        QuestionTitle = request.POST.get('QuestionTitle')
        QuestionType = request.POST.get('Icon-type')
        formID = request.session.get('questionnaire_id')
        ForQuestionnaire = Questionnaire.objects.get(id=formID) 
        question = Question.objects.create(title=QuestionTitle, question_type=QuestionType, for_questionnaire=ForQuestionnaire,has_weight=True, allow_doc=True ,weight=3)
        question.save()
       
        zQuestions = Question.objects.filter(for_questionnaire=formID)
        context = {'zQuestions': zQuestions, 'category': category}
        return render(request, 'addQuestions.html',context )
    
    return render(request, 'addQuestions.html', {'category': category})

    
    






#######  Skill Assessment Survey View #####

def skill_assessment_survey_view(request):
    context ={

    }
    return render(request,'SkillAssessmentSurvey.html',context)