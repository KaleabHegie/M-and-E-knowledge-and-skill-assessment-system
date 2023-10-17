from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from datetime import datetime
from .forms import CategoryForm
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
        return render(request, 'index.html', {'surveys': surveys})

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
        QuestionType = request.POST.get('IconType')
        formID = request.session.get('questionnaire_id')
        ForQuestionnaire = Questionnaire.objects.get(id=formID)
        weightInput = request.POST.get('weightInput')
        if weightInput > 0:
            has_weight = True
            weight = weightInput
        else:
            has_weight = False
            weight = None

        question = Question.objects.create(
            title=QuestionTitle, 
            question_type=QuestionType, 
            for_questionnaire=ForQuestionnaire,
            has_weight=has_weight, 
            allow_doc=True ,
            weight = weight
            )
        question.save()
       
        zQuestions = Question.objects.filter(for_questionnaire=formID)
        context = {'zQuestions': zQuestions, 'category': category}
        return render(request, 'addQuestions.html',context )
    
    return render(request, 'addQuestions.html', {'category': category})

    
    






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