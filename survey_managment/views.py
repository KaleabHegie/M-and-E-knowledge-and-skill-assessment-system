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
    surveys = Survey.objects.all().count()
    questions = Question.objects.all().count()
    Response = UserResponse.objects.all().count()

    context = {'surveys': surveys, 'questions': questions, 'Response':Response}
    return render(request, 'index.html', context)
    # survey_id = request.GET.get('survey_id')
    # if survey_id:
    #     survey = get_object_or_404(Survey, id=survey_id)
    #     questionnaires = survey.questionnaire_set.all()
    #     context = {
    #         'survey': survey,
    #         'questionnaires': questionnaires,
    #     }
    #     return render(request, 'index.html', context)
    # else:
    #     surveys = Survey.objects.all()
    #     count_survey = Survey.objects.all().count()
    #     context= {
    #         'surveys': surveys,
    #         'count_survey':count_survey,

    #     }
    #     return render(request, 'index.html',context)

# def loginView(request):
#     return render(request, 'login.html')

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
    


def questionCreationByType(request, survey_id):
    # survey_id = request.GET.get('survey_id')
    # survey = Survey.objects.get(id=survey_id)
    # survey_questions = survey.question.all()
    return render(request, 'addQuestions.html', {'survey_id':survey_id})


    
    

def newQuestion(request ,questionType ):
    categories = Category.objects.prefetch_related('subcategories')
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
 

        context = {'question': question,  'hasOption':hasOption }
        return render(request, 'addQuestions.html', context )
    


    context = {'questionType': questionType, 'categories': categories}
    return render(request, 'modal.html', context)







####### final preview views ################################

def greetingpage_view(request):
    context ={

    }
    return render(request, 'Final_Preview_Pages/greetingpage.html' , context)




@login_required
def survey_listss_views(request):
    today = date.today()
    user = request.user.Line_ministry
    surveys = Survey.objects.filter(start_at__lte=today, end_at__gte=today, for_line_ministry=user)
    data = {
        'surveys': surveys
    }
    return render(request, 'Final_Preview_Pages/SL.html', data)

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
        return redirect('survey_managment:surveys')
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



def compareDataView(request):
    return render(request, 'compare.html')