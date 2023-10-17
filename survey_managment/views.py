from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import *


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
        count_survey = Survey.objects.all().count()
        count_questionnaries = Questionnaire.objects.all().count()
        context= {
            'surveys': surveys,
            'count_survey':count_survey,
            'count_questionnaries':count_questionnaries
        }
        return render(request, 'index.html',context)

# def loginView(request):
#     return render(request, 'login.html')

def forgotPasswordView(request):
    return render(request, 'forgot-password.html')



def surveyCreationView(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()  # Save the form data to create a new Survey object
            print(survey.id)  # Check if the object has been saved to the database
            return redirect('survey_managment:chooseTarget', survey_id=survey.id , question_id = 0)  # Pass the survey ID to the success page
        else:
            print(form.errors)  # Print any validation errors
    else:
        form = SurveyForm()
    return render(request, 'surveyCreation.html', {'form': form})

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





def create_question(request , survey_id , questionnaire_id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        for question_id in selected_questions:
            question = Question.objects.get(id=question_id)
            # Create a new instance of the Question model with the same attributes as the selected question
            duplicated_question = Question.objects.create(
                title=question.title,
                label=question.label,
                question_type=question.question_type,
                for_questionnaire=question.for_questionnaire,
                choice_group=question.choice_group,
                choice=question.choice,
                category=question.category,
                has_weight=question.has_weight,
                weight=question.weight,
                allow_doc=question.allow_doc,
                doc_label=question.doc_label
            )
            # Do something with the duplicated question, such as saving it to the database or performing any other desired action
        return redirect("survey_managment:chooseSurvey" , survey_id)  # Redirect to a success page after processing the selected questions
    else:
        return redirect("survey_managment:displayQuestion" , survey_id , questionnaire_id)  # Redirect to an error page if the request method is not POST

    


def chooseSurvey(request , id=0):
    data = {
        'id':id,
        'questionnaires':  Questionnaire.objects.all(),
        'surveys': Survey.objects.all(),
        }
    return render(request, 'chooseSurvey.html' , data)




def displayQuestion(request, survey_id, questionnaire_id):
   
    
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        for question_id in selected_questions:
            question = get_object_or_404(Question, id=question_id)
            form = QuestionCreateByEdit(request.POST, instance=question)
            if form.is_valid():
                new_question = form.save(commit=False)
                new_question.for_questionnaire = questionnaire
                new_question.save()
                return redirect('survey_managment:index')
            else:
                print('Form is not valid:', form.errors)
        return redirect('survey_managment:chooseSurvey', id=survey_id)
    
    form = QuestionCreateByEdit()
    questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)
    questions = Question.objects.filter(for_questionnaire=questionnaire)
    data = {
        'questionnaire_id': questionnaire_id,
        'questions': questions,
        'form': form,
    }
    
    return render(request, 'displayQuesion.html', data)


    


def chooseTarget(request, survey_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('survey_managment:chooseTarget' , survey_id=survey.id  , question_id = question.id )
    else:
        form = QuestionForm(instance=question)
    
    data = {
        'form': form,
        'question_id': question_id,
        'survey_id': survey_id,
        'questions': Question.objects.all()
    }
    
    return render(request, 'chooseTarget.html', data)


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




def display_questionnaire(request, questionnaire_id):
    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    questions = Question.objects.filter(for_questionnaire=questionnaire)
    print("Number of questions retrieved:", questions.count())  
    return render(request, 'Analysis_for_each.html', {'questionnaire': questionnaire, 'questions': questions})