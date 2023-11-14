from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Category, Question
from django.http import JsonResponse

from django.core.paginator import Paginator
from datetime import date




from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from datetime import datetime
from .forms import CategoryForm
from .forms import *


from .models import *

from django.contrib.auth.decorators import login_required


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



def indexView(request):
    survey_id = request.GET.get('survey_id')
    if survey_id:
        survey = get_object_or_404(Survey, id=survey_id)
        questionnaires = survey.question_set.all()
        context = {
            'survey': survey,
            'questionnaires': questionnaires,
        }
        return render(request, 'index.html', context)
   
    else:
        surveys = Survey.objects.all()
        surveyType = SurveyType.objects.all()
        surveys_count = Survey.objects.all().count()
        questions = Question.objects.all().count()
        Response = UserResponse.objects.all().count()
        line_ministry = Line_ministry.objects.all()
        form = AnalysisForm()
       
   



        context = {'surveys_count': surveys_count, 'questions': questions, 'Response':Response , 'surveys':surveys ,
             'line_ministry':line_ministry,'form':form,'surveyType':surveyType}
      
        return render(request, 'index.html', context)

def load_survey(request):
    survey_type_id = request.GET.get("survey_type")
    survey = Survey.objects.filter(survey_type_id=survey_type_id)
   
    return render(request ,"load_survey.html",{"survey":survey , })

def load_ministry(request):
    survey_id = request.GET.get("survey")
    survey = Survey.objects.filter(id=survey_id).first()
    line_ministries = survey.for_line_ministry.all() if survey else []
    return render(request, "load_ministry.html", {"line_ministries": line_ministries})


from django.shortcuts import render
from django.http import JsonResponse
import json

from django.http import JsonResponse
from .models import Survey, Line_ministry, CustomUser, Category, Department, Question, SurveyType, UserResponse

def get_data(request):
    surveys = Survey.objects.all()
    data1 = []
    data2 = []

    
    for survey in surveys:
        line_ministries = survey.for_line_ministry.all()
        line_ministry_data = []
        
        for line_ministry in line_ministries:
            line_ministry_data.append({
                'id': line_ministry.id,
                'name': line_ministry.name
            })
        
        survey_data = {
            'id': survey.id,
            'name': survey.name,
            'line_ministries': line_ministry_data
        }
        
        data1.append(survey_data)

    for survey in surveys:
            for_question = survey.question.all()
            question_data = []
        
            for question in for_question:
                question_data.append({
                    'id': question.id ,
                    'name': question.title ,
                })
            
            surveys_data = {
                'id': survey.id,
                'name': survey.name,
                'questions': question_data
            }
            
            data2.append(surveys_data)
    
    serialized_data = {
        'answer': list(Answer.objects.values()),
        'surveys': data1,
        'survey_questions' : data2 ,
        'line_ministry': list(Line_ministry.objects.values('id', 'name')),
        'users': list(CustomUser.objects.values()),
        'category': list(Category.objects.values()),
        'department': list(Department.objects.values()),
        'questions': list(Question.objects.values()),
        'survey_type': list(SurveyType.objects.values()),
        'survey': list(Survey.objects.values()),
        'user_response': list(UserResponse.objects.values())

    }
    
    return JsonResponse(serialized_data, safe=False)


def forgotPasswordView(request):
    return render(request, 'forgot-password.html')



def surveyCreationView(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            survey = form.save()  
            print(survey.id)  # Check if the object has been saved to the database
            # redirect_url = f'survey_managment:questionCreationByType/?survey_id=survey.id'
            return redirect('survey_managment:questionCreationByType',survey_id=survey.id )  # Pass the survey ID to the success page
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



def jsonSender(request):
    data = {
        'questions' : list(Question.objects.all().values()),
        'categories': list(Category.objects.all().values()),
        'surveys':    list(Survey.objects.all().values()),
    }
    return JsonResponse(data)

def surveyQuestionnaireView(request):
    surveys = Survey.objects.all()

    data = {
        'surveys': surveys,
        'categories' : Category.objects.all()
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


def user_response_list(request, id):
    survey = get_object_or_404(Survey, id=id)
    user_responses = UserResponse.objects.filter(forsurvey=survey)
    data = {
        'survey_id': id,
        'survey': survey,
        'user_responses': user_responses,
    }
    return render(request, 'user_response_list.html', data)


def user_response(request, id , response_id):
    survey = get_object_or_404(Survey, id=id)
    user_responses = UserResponse.objects.filter(forsurvey=survey)
    answers = Answer.objects.filter(response__in=user_responses)
    data = {
        'survey_id': id,
        'survey': survey,
        'user_responses': user_responses,
        'answers': answers,
        'response_id' : response_id
    }
    return render(request, 'user_response.html', data)



def survey_detail(request, id):
    data = {
        'survey_id': id,
        'survey': Survey.objects.get(id=id),
        'user_responses': UserResponse.objects.filter(forsurvey_id=id),
        'questions': Survey.objects.get(id=id).question.all()
    }
    return render(request, 'survey_detail.html', data)

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

def chooseSurvey(request , id , choose_id ):
    data = {
        'choose_id':choose_id,
        'survey_id':id,
        'surveys': Survey.objects.all(),
        }
    return render(request, 'chooseSurvey.html' , data)




def displayQuestion(request, id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        survey = get_object_or_404(Survey, id=id)
        for question_id in selected_questions:
            ques = get_object_or_404(Question, id=question_id)
            
            survey.question.add(ques)
          
        return redirect('survey_managment:questionCreationByType' , survey_id=id)
    else:
        data = {
            'questions': Question.objects.all(),
            'page_number': request.GET.get('page'),
            'questionss': Paginator(Question.objects.all(), 4).get_page(request.GET.get('page')),
            'paginator': Paginator(Question.objects.all(), 4),
            'surveys': Survey.objects.get(id=id),
            'categories': Category.objects.all(),
            'id' : id,
        }

    return render(request, 'displayQuesion.html', data)


def catagorizedQuestion(request, id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        survey = get_object_or_404(Survey, id=id)
        for question_id in selected_questions:
            ques = get_object_or_404(Question, id=question_id)
            survey.question.add(ques)
        return redirect('survey_managment:Index')
    else:
        data = {
            'questions': Question.objects.all(),
            'page_number': request.GET.get('page'),
            'questions': Paginator(Question.objects.all(), 4).get_page(request.GET.get('page')),
            'paginator': Paginator(Question.objects.all(), 4),
            'surveys': Survey.objects.get(id=id),
            'id' : id,
            'categories': Category.objects.all(),
        }

    return render(request, 'catagorizedQuestion.html', data)





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
        'questions': Question.objects.all(),
    }
    
    return render(request, 'chooseTarget.html', data)


 # survey_id = request.GET.get('survey_id')
    # survey = Survey.objects.get(id=survey_id)
    # survey_questions = survey.question.all()
def questionCreationByType(request, survey_id):
    zsurvey = Survey.objects.get(id=survey_id)
    questions = zsurvey.question.all()
    return render(request, 'addQuestions.html', {'zsurvey':zsurvey, 'questions' : questions})
 
    

def newQuestion(request,questionType, s_id ):
    categories = Category.objects.prefetch_related('subcategories')
    survey = get_object_or_404(Survey, id=s_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        label = request.POST.get('labelInput')
        question_type = request.POST.get('question_type')
        has_weight = bool(request.POST.get('weightCHK'))
        weight = int(request.POST.get('weightInput')) if has_weight else None
        allow_doc = bool(request.POST.get('allow_doc'))
        doc_label = request.POST.get('doc_label')
        selected_category_id = request.POST.get('category')

        category = get_object_or_404(Category, id=selected_category_id)

        question = Question.objects.create(
            title=title,
            label=label,
            question_type=question_type,
            has_weight=has_weight,
            weight=weight,
            allow_doc=allow_doc,
            doc_label=doc_label,
            category=category,
        )

        hasOption = ['choice', 'radio']
        if question_type in hasOption:
            options = request.POST.getlist('option')
            for i in options:
                newChoice = Choice.objects.create(name=i)
                question.choice.add(newChoice)

        question.save()
        
        survey.question.add(question)
        return redirect('survey_managment:questionCreationByType', survey_id=s_id )


    context = {'questionType': questionType, 'categories': categories}
    return render(request, 'modal.html', context)







####### final preview views ################################
@login_required
def greetingpage_view(request):
    context ={
        
    }
    return render(request, 'Final_Preview_Pages/greetingpage.html' , context)




@login_required
def survey_listss_views(request):
    today = date.today()
    surveys = Survey.objects.filter(start_at__lte=today, end_at__gte=today)
    data = {
        'surveys': surveys
    }
    return render(request, 'Final_Preview_Pages/SL.html', data)

@login_required
def questionForSurvey(request, id):
    survey = get_object_or_404(Survey, id=id)
    questions = survey.question.all()
    print(request.user)
    if request.method == 'POST':
        user_response_form = UserResponseForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(question.id)) for question in survey.question.all()]
        # value = request.POST.get('answer_16')
        # print(value)

        userresponse = UserResponse.objects.create(forsurvey = survey , submitted_by = request.user)
        for i in questions:
            value = request.POST.get(f'answer_{i.id}')
            Answer.objects.create(forquestion = i , answertext = value , response = userresponse)              
            value = ''
        return redirect('survey_managment:surveylists')
    else:
        user_response_form = UserResponseForm()
        answer_forms = [AnswerForm(prefix=str(question.id)) for question in survey.question.all()]

    context = {
        'survey': survey,
        'questions': questions,
        'user_response_form': user_response_form,
        'answer_forms': answer_forms,
    }

    return render(request, 'Final_Preview_Pages/questionForSurvey.html', context)





def anonymous_survey_listss_views(request):
    today = date.today()
    survey_type = SurveyType.objects.get(name='For Employee')
    surveys = Survey.objects.filter(start_at__lte=today, end_at__gte=today , survey_type =  survey_type)
    print(surveys)
    data = {
        'surveys': surveys
    }
    return render(request, 'Final_Preview_Pages/SL_Anonymous.html', data)

def questionForSurveyAnonymous(request, id):
    survey = get_object_or_404(Survey, id=id)
    questions = survey.question.all()
    if request.method == 'POST':
        anonymous_user_response_form = AnonymousUserResponseForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(question.id)) for question in survey.question.all()]
        # value = request.POST.get('answer_16')
        # print(value)

        anonymous_user_response = UserResponse.objects.create(forsurvey = survey , year_of_experiance = request.year_of_experiance , department = request.department , age = request.age)
        for i in questions:
            value = request.POST.get(f'answer_{i.id}')
            Answer.objects.create(forquestion = i , answertext = value , response = anonymous_user_response)              
            value = ''
        return redirect('survey_managment:index')
    else:
        anonymous_user_response_form = AnonymousUserResponseForm()
        answer_forms = [AnswerForm(prefix=str(question.id)) for question in survey.question.all()]

    context = {
        'survey': survey,
        'questions': questions,
        'anonymous_user_response_form': anonymous_user_response_form,
        'answer_forms': answer_forms,
    }

    return render(request, 'Final_Preview_Pages/surveyForAnonymous.html', context)



def compareDataView(request):
    return render(request, 'compare.html')