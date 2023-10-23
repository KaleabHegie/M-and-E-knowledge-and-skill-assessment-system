from django.shortcuts import get_object_or_404, render, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Category, Question
from django.http import JsonResponse


def category_questions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        questions = Question.objects.filter(category_id=category_id)
        question_list = []
        for question in questions:
            question_list.append({
                'id': question.id,
                'text': question.text,
                # Add more fields as needed
            })
        return JsonResponse({'questions': question_list})
    categories = Category.objects.all()
    return render(request, 'category_questions.html', {'categories': categories})


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



def indexView(request):
     return render(request, 'index.html')
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
            return redirect('survey_managment:questionCreationByType', survey_id=survey.id)  # Pass the survey ID to the success page
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



def jsonSender(request, id):
    data = {
        'questions' : list(Question.objects.all().values()),
        'categories': list(Category.objects.all().values()),
        'surveys': Survey.objects.get(id=id),
    }
    return JsonResponse(data)

def surveyQuestionnaireView(request, id):

    data = {
        'id':id,
        'surveys': Survey.objects.get(id=id),
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

    


def chooseSurvey(request , id , choose_id ):
    data = {
        'choose_id':choose_id,
        'survey_id':id,
        'surveys': Survey.objects.all(),
        }
    return render(request, 'chooseSurvey.html' , data)




def displayQuestion(request, survey_id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        survey = get_object_or_404(Survey, id=survey_id)
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
            'surveys': Survey.objects.get(id=survey_id),
            'categories': Category.objects.all(),
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

def questionCreationByType(request , survey_id):
    category = Category.objects.all()
    
    if request.method == 'POST':
        QuestionTitle = request.POST.get('QuestionTitle')
        QuestionType = request.POST.get('IconType')
        weightInput = request.POST.get('weightInput')
        if int(weightInput) > 0:
            has_weight = True
            weight = weightInput
        else:
            has_weight = False
            weight = None

        question = Question.objects.create(
            title=QuestionTitle, 
            question_type=QuestionType, 
            has_weight=has_weight, 
            allow_doc=True ,
            weight = weight
            )
        question.save()

        
        
       
       
        context = {'category': category , 'survey_id':survey_id}
        return render(request, 'addQuestions.html',context )
    
    return render(request, 'addQuestions.html', {'category': category , 'survey_id':survey_id})

    
    






# def userinfo_view(request):
#     context = {}
#     return render(request, 'userinfopageforsurvey.html', context)

# def skill_assessment_survey_view(request):
#     Question_list = Question.objects.all()
#     Catagory_list = Category.objects.all()
#     context ={
#       'Question_list':Question_list ,'Catagory_list':Catagory_list
#     }
#     return render(request,'SkillAssessmentSurvey.html',context)

# def answer_question(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     if request.method == 'POST':
#         answer_text = request.POST.get('answer')
#         answer = Answer(question=question, text=answer_text)
#         answer.save()
#         return redirect('surveydisplay')
#     return render(request, 'answer_question.html', {'question': question})





# def category_questions(request):
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         questions = Question.objects.filter(category_id=category_id)
#         question_list = []
#         for question in questions:
#             question_list.append({
#                 'id': question.id,
#                 'text': question.text,
#             })
#         return JsonResponse({'questions': question_list})
#     categories = Category.objects.all()
#     return render(request, 'SkillAssessmentSurvey.html', {'categories': categories})


def display_questionnaire(request, questionnaire_id):
    print("Number of questions retrieved:", questions.count())  
    return render(request, 'Analysis_for_each.html', {'questionnaire': questionnaire, 'questions': questions})




####### final preview views ################################

def greetingpage_view(request):
    context ={

    }
    return render(request, 'Final_Preview_Pages/greetingpage.html' , context)

def skill_ass_sur_view(request,):
    question_list = Question.objects.all()
    context ={
           'question_list': question_list
    }
    return render(request, 'Final_Preview_Pages/Skill_Ass_Sur_Preview.html' , context)

def line_min_sur_view(request):
    context ={

    }
    return render(request, 'Final_Preview_Pages/Line_Min_Sur_Preview.html' , context)




def compareDataView(request):
    return render(request, 'compare.html')