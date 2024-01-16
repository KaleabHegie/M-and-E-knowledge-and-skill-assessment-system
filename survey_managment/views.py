from audioop import reverse
import re
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Category, Question
from datetime import date, datetime
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json



# Create your views here.

def new_page(request):
    return render(request,'new_create.html')

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
        survey_years = Survey.objects.order_by('created_at__year').values('created_at__year').distinct() 
        form = AnalysisForm()
       
   



        context = {'surveys_count': surveys_count, 'questions': questions, 'Response':Response , 'surveys':surveys ,
             'line_ministry':line_ministry,'form':form,'surveyType':surveyType,'survey_years':survey_years}
      
        return render(request, 'index.html', context)
def ministries(request):
    
    return render(request , 'ministries.html')

def filter(request):
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
        survey_years = Survey.objects.order_by('created_at__year').values('created_at__year').distinct() 
        form = AnalysisForm()
       
        



        context = {'surveys_count': surveys_count, 'questions': questions, 'Response':Response , 'surveys':surveys ,
             'line_ministry':line_ministry,'form':form,'surveyType':surveyType,'survey_years':survey_years}
      
        return render(request, 'filter.html', context)

####### Message Views ################################

def average(request):
    return render(request , 'averages.html' )

def inbox(request):
    if request.method == 'POST':
        if 'trash' in request.POST:
            messageIds = request.POST.getlist('messageId')
            print(messageIds)
            for messageId in messageIds:
                message = ContactUs.objects.get(id=messageId)
                print('hello')
                message.status = 'trash'
                message.save()
            return redirect('survey_managment:trash')
        else:
            pass
    else:
        context = {
            'message': ContactUs.objects.filter(status='inbox')
        }
        return render(request, "inbox.html", context)
    

def sent(request):  
    if request.method == 'POST':
        if 'trash' in request.POST:
            messageIds = request.POST.getlist('messageId')
            print(messageIds)
            for messageId in messageIds:
                message = ContactUs.objects.get(id=messageId)
                print('hello')
                message.status = 'trash'
                message.save()
            return redirect('survey_managment:trash')
        else:
            pass
    else:  
       context = {
           'message' : ContactUs.objects.filter(status = 'sent')
       }
       return render(request ,"sent.html" , context)


def draft(request):  
    if request.method == 'POST':
        if 'trash' in request.POST:
            messageIds = request.POST.getlist('messageId')
            print(messageIds)
            for messageId in messageIds:
                message = ContactUs.objects.get(id=messageId)
                print('hello')
                message.status = 'trash'
                message.save()
            return redirect('survey_managment:trash')
        else:
            pass
    else:  
      context = {
          'message' : ContactUs.objects.filter(status = 'draft')
      }
      return render(request ,"draft.html" , context)


def trash(request):    
    if request.method == 'POST':
        if 'trash' in request.POST:
            messageIds = request.POST.getlist('messageId')
            print(messageIds)
            for messageId in messageIds:
                message = ContactUs.objects.get(id=messageId)
                message.delete()
            return redirect('survey_managment:trash')
        else:
            pass
    else:  
      context = {
          'message' : ContactUs.objects.filter(status = 'trash')
      }
      return render(request ,"trash.html" , context)


def compose(request):
    if request.method == 'POST':
      if 'send' in request.POST:  
        form_data = request.POST
        to = form_data['to']
        subject = form_data['subject']
        message = form_data['message']
        user = request.user
        # Create a new message object
        new_message = ContactUs(name = user , email = user.email , subject=subject , message=message , status= 'sent')
        new_message.save()
        try:
            validate_email(to)
        except ValidationError:
            # Invalid email address
            error_message = "Invalid email address"
            return render(request, 'compose.html', {'error_message': error_message})
        
        # Send the email
        send_mail(
            subject,
            message,
            'benjiyg400@gmail.com',  # Replace with your email address
            [to],
            fail_silently=False,
        )
        return redirect( 'survey_managment:sent')
      else:
        form_data = request.POST
        to = form_data['to']
        subject = form_data['subject']
        message = form_data['message']
        user = request.user
        # Create a new message object
        new_message = ContactUs(name = user , email = user.email , subject=subject , message=message , status= 'draft')
        new_message.save()
        return redirect( 'survey_managment:draft')
    else:
        # Render the initial form
        return render(request, 'compose.html')


def reply_to_message(request, message_id):
    message = get_object_or_404(ContactUs, id=message_id)

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        user = request.user

        if form.is_valid():
            cleaned_data = form.cleaned_data

            subject = cleaned_data['subject']
            body = cleaned_data['message']
            recipient_list = [message.email]
            sender = user.email

            send_mail(subject, body, sender, recipient_list)

           
            ContactUs.objects.create(
                email=message.email,
                subject=f"RE: {message.subject}",
                message=message.message,
                status='sent'
            )

            # Redirect to a success page or display a success message
            return render(request, 'sent.html')
    else:
        initial_data = {'subject': f"RE: {message.subject}", 'message': message.message}
        form = ContactUsForm(initial=initial_data)

    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'reply_form.html', context)


def read(request , id):
    message = get_object_or_404(ContactUs, id=id)  
    message.read = True  # Update the read field to True
    message.save() 
    if request.method == 'POST': 
      if 'delete' in request.POST:  
        messageId = request.POST.get('messageId')
        print(messageId)
        message = ContactUs.objects.get(id=messageId)
        message.status = 'trash'
        message.save()
        return redirect( 'survey_managment:trash')
      else:
       pass
    else : 
        context = {
            'message' : ContactUs.objects.get(id=id)
    
        }
        return render(request ,"read.html" , context)



####### User Views ################################



def user_profile(request):
    return render(request , 'profile.html' )


def edit_profile(request):
    return render(request , 'edit_profile.html' )


def users(request):
    return render(request , 'user.html' )


def forgotPasswordView(request):
    return render(request, 'forgot-password.html')


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





####### Analsis views ################################



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


def compareDataView(request):
    line_ministry = Line_ministry.objects.all()
    survey_type = SurveyType.objects.all()
    survey = Survey.objects.all()
    survey_years = Survey.objects.order_by('created_at__year').values('created_at__year').distinct() 


    context = {
        'line_ministry':line_ministry,
        'survey_type': survey_type,
        'survey':survey,
        'survey_years':survey_years
    }
    return render(request, 'compare.html',context)


def get_data(request):
    surveys = Survey.objects.all()
    data1 = []
    data2 = []
    data3 = []
    data4 = []

    userResponse = UserResponse.objects.all()
    for response in userResponse:
        respone_data = {
            "id": response.id,
            "forsurvey_id": response.forsurvey_id,
            "submitted_by_id":response.submitted_by_id ,
            "submitted_by_lineMinistry": ["hello"],
            "submitted_at": response.submitted_at,
            "year_of_experiance": response.year_of_experiance,
            "department": response.department,
            "age": response.age,
            "status": response.status,
            "line_ministry_id": response.line_ministry_id,
        }
        try:
            user = CustomUser.objects.get(id=response.submitted_by_id)
            line_ministry = user.Line_ministry.id
            respone_data["submitted_by_lineMinistry"] = str(line_ministry)
        except CustomUser.DoesNotExist:
            respone_data["submitted_by_lineMinistry"] = None

        data4.append(respone_data)
    categories = Category.objects.all()

    for catagory in categories:
        catagory_data = {
           "name": catagory.name,
           "has_parent": catagory.parent is not None ,
            "parent_name" : catagory.parent.name if catagory.parent else None,
            "questions" : []
        }
        questions = catagory.question_set.all()
        for question in questions:
            answer = question.id
            catagory_data["questions"].append(answer)
        data3.append(catagory_data)
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
    questions = []
    for question_obj in Question.objects.all():
        question_info = {
            'id' : question_obj.id,
            'title': question_obj.title,
            'has_category': question_obj.category is not None if question_obj.category else None,
            'category_name': question_obj.category.name if question_obj.category else None,
            'category_id': question_obj.category.id if question_obj.category else None,
            'has_parent': question_obj.category.parent is not None if question_obj.category else None,
            'parent_name': question_obj.category.parent.name if question_obj.category and question_obj.category.parent else None,
            'parent_id': question_obj.category.parent.id if question_obj.category and question_obj.category.parent else None,
            "label": question_obj.label,
            "question_type": question_obj.question_type,
            "has_weight": question_obj.has_weight,
            "weight": question_obj.weight,
            "allow_doc": question_obj.allow_doc,
            "doc_label": question_obj.doc_label,
            "order": question_obj.order
        }
        questions.append(question_info)
            
    serialized_data = {
        'answer': list(Answer.objects.values()),
        'surveys': data1,
        'survey_questions' : data2 ,
        'questions_with_their_category': data3,
        'line_ministry': list(Line_ministry.objects.values('id', 'name')),
        'users': list(CustomUser.objects.values()),
        'category': list(Category.objects.values()),
        'department': list(Department.objects.values()),
        'questions': questions,
        'survey_type': list(SurveyType.objects.values()),
        'survey': list(Survey.objects.values()),
        'user_response': data4,

    }
    
    return JsonResponse(serialized_data, safe=False)



####### Survey , User Response and Question views ################################



def survey(request):
    data = {
        'surveys_employee': Survey.objects.filter(survey_type__name = "For Employee"),
        'surveys_org': Survey.objects.filter(survey_type__name ="For Organization"),
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


def user_response(request, id, response_id):
    survey = get_object_or_404(Survey, id=id)
    user_responses = UserResponse.objects.filter(id=response_id)
    answers = Answer.objects.filter(response__in=user_responses)
    documents = Document.objects.all()     
    if request.method == 'POST':
     if 'approve' in request.POST:  
        survey = get_object_or_404(Survey, id=id)
        userresponses = get_object_or_404(UserResponse, id=response_id)
        userresponses.status = 'approved'
        userresponses.save()
        user_responses = UserResponse.objects.filter(id=response_id)
        answers = Answer.objects.filter(response__in=user_responses)
        for answer in answers:
            answer.recommendation = ''
            answer.save()
        messages.success(request , 'Succussesfuly approved')
        data = {
              'survey_id': id,
              'survey': survey,
              'user_responses': user_responses,
              'answers': answers,
              'response_id' : response_id
                }
        return render(request, 'user_response.html', data)
       
     if 'done' in request.POST:
        survey = get_object_or_404(Survey, id=id)
        userresponses = get_object_or_404(UserResponse, id=response_id)
        data = {
              'survey_id': id,
              'survey': survey,
              'user_responses': user_responses,
              'answers': answers,
              'response_id' : response_id
                }
        userresponses.status = 'recomended'
        return redirect('survey_managment:survey_detail' , id)
     else :  
        recommendation = request.POST.get('recommendation')
        checkedResponse = request.POST.get('checkedResp') # the checkbox value holding the answer id to be recommended
        theAnswer = Answer.objects.filter(id=checkedResponse)     # the answer to be recommended
        theAnswer.update(recommendation=recommendation)
    data = {
        'survey_id': id,
        'survey': survey,
        'user_responses': user_responses,
        'answers': answers,
        'documents': documents,
        'response_id': response_id
    }
    return render(request, 'user_response.html', data)


def survey_detail(request, id):
    data = {
        'survey_id': id,
        'survey': Survey.objects.get(id=id),
        'user_responses': UserResponse.objects.filter(forsurvey_id=id),
        'questions': Survey.objects.get(id=id).question.all(),
        'line_ministries' : Survey.objects.get(id=id).for_line_ministry.all()
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


def questionCreationByType(request, survey_id):
    zsurvey = Survey.objects.get(id=survey_id)
    questions = zsurvey.question.all()
    pattern = r'/newQuestion/[^/]+/\d+/'
    if request.META.get('HTTP_REFERER') and '/surveyCreation' in request.META['HTTP_REFERER']:
        messages.success(request, 'Survey created successfully. Add questions to it.')  # regular expression pattern to match the URL
    if request.META.get('HTTP_REFERER') and re.search(pattern, request.META['HTTP_REFERER']):
        messages.success(request, 'Survey created successfully. Add questions to it.')    
    
    return render(request, 'addQuestions.html', {'zsurvey': zsurvey, 'questions': questions})
   

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

    # elif request.method == 'POST' and request.POST.get("categoryForm"):
    #         s_id = request.POST.get('s_id')
    #         questionType = request.POST.get('questionType')
    #         newCategory = request.POST.get('newCategory')
    #         subcategoriesNEW = request.POST.get('subcategoriesNEW')

    #         newCate = Category.objects.create(name=newCategory)

    #         if subcategoriesNEW:
    #             zparent = Category.objects.get(id=newCate.id)
    #             for i in subcategoriesNEW:
    #                 Category.objects.create(name=i, parent=zparent)

    context = {'questionType': questionType, 'categories': categories}
    return render(request, 'modal.html', context)


def QuestionCategories(request):
    categories = Category.objects.all()
    context = {'categories' : categories}

    if request.method == 'POST':
        zcategory = request.POST.get('zcategory')
        parent = request.POST.get('parent')

        if parent:
            Category.objects.create(name=zcategory, parent=parent)
        else:
            Category.objects.create(name=zcategory)
        

    return render(request, 'category.html', context)


def load_survey(request):
    survey_type_id = request.GET.get("survey_type")
    survey = Survey.objects.filter(survey_type_id=survey_type_id)
   
    return render(request ,"load_survey.html",{"survey":survey  })


def pending_response(request):
    user_responses = UserResponse.objects.filter(status='pending')
    responses = UserResponse.objects.filter(status='pending').count()
    data = {
        'user_responses': user_responses,
        "responses" : responses,
    }
    return render(request , 'pendingResponse.html' , data )


def load_ministry(request):
    survey_id = request.GET.get("survey")
    survey = Survey.objects.filter(id=survey_id).first()
    line_ministries = survey.for_line_ministry.all() if survey else []
    return render(request, "load_ministry.html", {"line_ministries": line_ministries})


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








####### final preview views ################################

@login_required
def greetingpage_view(request):
    
    user = request.user 
    user = CustomUser.objects.get(username = user)
    line_ministry = request.user.Line_ministry
    if request.method == 'POST':
        # Create a new instance of the ContactUs model
        contact = ContactUs()

        # Assign form data to the corresponding fields
        contact.name = request.POST.get('name')
        contact.email = request.POST.get('email')
        contact.subject = request.POST.get('subject')
        contact.message = request.POST.get('message')
        contact.status = 'inbox'
        line_ministry = request.user.Line_ministry
        user = request.user 
        user = CustomUser.objects.get(username = user)
    

        # Save the new object to the database
        contact.save()
        messages.success(request, 'Thank you for contacting us. Your Message is submitted succussesfuly.')
    context ={
        'surveys_count' : Survey.objects.filter(userresponse__status='recomended', for_line_ministry = line_ministry , userresponse__submitted_by = user).count(),
    }
    
    return render(request, 'Final_Preview_Pages/greetingpage.html' , context)



@login_required
def survey_listss_views(request):
    user = request.user
    user_responses = UserResponse.objects.filter(submitted_by=user)
    surveys_with_responses = [response.forsurvey for response in user_responses]

    user = CustomUser.objects.get(username=user)
    line_ministry = user.Line_ministry
    surveys = Survey.objects.filter(for_line_ministry=line_ministry)
    surveys_without_responses = surveys.exclude(id__in=[survey.id for survey in surveys_with_responses])
    pattern = r'/questionForSurvey/\d+/'
    pattern1 = r'/questionForSurveyAnonymous/\d+/\d+/'
    if request.META.get('HTTP_REFERER') and re.search(pattern, request.META['HTTP_REFERER']):
        messages.success(request, 'Your Survey  is submitted succussesfuly.') 
        print("hello") # regular expression pattern to match the URL
    if request.META.get('HTTP_REFERER') and re.search(pattern1, request.META['HTTP_REFERER']):
        messages.success(request, 'Your Survey is submitted succussesfuly.')    
    

    data = {
        'surveys': surveys_without_responses
    }
    return render(request, 'Final_Preview_Pages/SL.html', data)



@login_required
def questionForSurvey(request, id):
    survey = get_object_or_404(Survey, id=id)
    questions = survey.question.all()
    cat_list = []
    for cat in Category.objects.all():
        question_filtered = survey.question.filter(category=cat)
        questions_list = []
        for question in question_filtered:
            questions_list.append(question.title)
        cat_list.append({"category":cat.name,"questions":questions_list})
    
    question_cat_none = survey.question.filter(category=None)
    questions_list = []
    for question in question_cat_none:
        questions_list.append(question)
    cat_list.append({"category":'No category',"questions":questions_list})

    if request.method == 'POST':
        user_response_form = UserResponseForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(question.id)) for question in survey.question.all()]
        document_forms = [DocumentForm(request.POST, request.FILES, prefix=str(question.id)) for question in survey.question.all()]
        userresponse = UserResponse.objects.create(forsurvey = survey , submitted_by = request.user)
        for category in cat_list:
            for question_title in category['questions']:
                question = Question.objects.get(title=question_title)
                print(question)
                answer_text = request.POST.get(f'answer_{question.id}')
                answer = Answer.objects.create(response=userresponse, forquestion=question, answertext=answer_text)
                answer.save()
                file = request.FILES.get(f'file_{question.id}')   
                document = Document(foranswer=answer, document=file)   
                document.save()
              
        return redirect('survey_managment:surveylists')
    else:
        user_response_form = UserResponseForm()
        answer_forms = [AnswerForm(prefix=str(question.id)) for question in survey.question.all()]
        document_forms = [DocumentForm(prefix=str(question.id)) for question in survey.question.all()]    
    context = {
        'survey': survey,
        'cat_list': cat_list,
        'questions': questions,
        'user_response_form': user_response_form,
        'answer_forms': answer_forms,
        'document_forms' : document_forms,
    }

    return render(request, 'Final_Preview_Pages/questionForSurvey.html', context)


@login_required
def recomended_survey_list(request):
    today = date.today()
    user = request.user 
    user = CustomUser.objects.get(username = user)
    line_ministry = request.user.Line_ministry
    print(user)
    print(line_ministry)
    data = {
        "surveys" : Survey.objects.filter(userresponse__status='recomended', for_line_ministry = line_ministry , userresponse__submitted_by = user)
        }
    return render(request, 'recomended_survey_list.html', data)



@login_required
def recomended_survey(request, id):
    survey = get_object_or_404(Survey, id=id)
    user = request.user
    response = get_object_or_404(UserResponse, forsurvey=survey, submitted_by=user)

    questions = Question.objects.filter(survey=survey)
    answers = []
    documents = []
    for question in questions:
       ans = Answer.objects.get(response = response , forquestion = question )
       answers.append(Answer.objects.get(response = response , forquestion = question ))
       try :
          documents.append(Document.objects.get(foranswer = ans ))
       except :
          pass
    # print(question , answers)
    if request.method == 'POST':
        answer_set = request.POST.getlist('answer_set')
        document_set = request.FILES.getlist('document_set')
        print(document_set)
        print(answer_set)
        for i, answer  in enumerate(answers):
          try:
              obj = Answer.objects.get(id=answer.id)
              obj.answertext = answer_set[i]
              obj.save()
          except :
              pass
        for i, document in enumerate(documents):
           print(document)
           try:
              objDoc = Document.objects.get(id=document.id)
              objDoc.document = document_set[i]
              print(document)
              objDoc.save()
           except :
              pass
        return redirect ("survey_managment:recomended_survey_list")   

    context = {
        "questions" : questions , 
        "answers" : answers,
        "survey"  : survey,
        "documents" : Document.objects.all()
    }
    return render(request, 'recomended_survey.html', context)


@login_required
def previous_analysis(request ):
    previous_responses = UserResponse.objects.filter(submitted_by=request.user)

    context = {
        'previous_responses': previous_responses
    }
    return (request , 'previous_analysis.html' , context )



def user_info(request):
    if request.method == 'POST':
        form = UserResponseFormA(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.save()
            user_response_id = response.id   # Get the line ministry of the saved UserResponse object
            return redirect('survey_managment:anonymous_survey_listss_views', user_response_id=user_response_id)  # Pass the line ministry as a parameter
    else:
        form = UserResponseFormA()
    data = {
        'form': form,
    }
    return render(request, 'Final_Preview_Pages/userinfopage.html', data)



def anonymous_survey_listss_views(request , user_response_id):
    today = date.today()
    survey_type = SurveyType.objects.get(name='For Employee')
    user_response = UserResponse.objects.get(id=user_response_id )
    line_ministry = user_response.line_ministry
    surveys = Survey.objects.filter(survey_type =  survey_type , for_line_ministry = line_ministry)
    data = {
        'surveys': surveys,
        'user_response_id' : user_response_id
    }
    return render(request, 'Final_Preview_Pages/SL_Anonymous.html', data)



def questionForSurveyAnonymous(request, id , user_response_id):
    survey = get_object_or_404(Survey, id=id)
    questions = survey.question.all()
    user_response = UserResponse.objects.get(id=user_response_id)
    if request.method == 'POST':
        anonymous_user_response_form = AnonymousUserResponseForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(question.id)) for question in survey.question.all()]
        # value = request.POST.get('answer_16')
        # print(value)

        if user_response.forsurvey :
           user_response = UserResponse.objects.create(
           forsurvey=survey,
           department=user_response.department,
           age=user_response.age,
           year_of_experiance = user_response.year_of_experiance,
           status='approved',
    )

           user_response.save() 
           for i in questions:
               value = request.POST.get(f'answer_{i.id}')
               Answer.objects.create(forquestion = i , answertext = value , response = user_response)              
               value = ''
           
           return redirect('survey_managment:anonymous_survey_listss_views' , user_response_id=user_response_id)
        else :
           user_response.status = 'approved'
           user_response.forsurvey = survey
           user_response.save() 
           for i in questions:
               value = request.POST.get(f'answer_{i.id}')
               Answer.objects.create(forquestion = i , answertext = value , response = user_response)              
               value = ''
          
           return redirect('survey_managment:anonymous_survey_listss_views' , user_response_id=user_response_id)
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

import json
def createQuestion(request,survey_id ):
    zsurvey = Survey.objects.get(id=survey_id)
    categories = Category.objects.all()
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
            objects_json = request.POST.get('objects')
            objects = json.loads(objects_json)
            for obj in objects:
                category_id = obj['category']
                category = get_object_or_404(Category ,id=category_id)
                has_weight= obj['hasWeight']
                has_doc = obj['hasDoc']
                if has_weight=="on":
                    has_weight= True  
                else:
                    has_weight= False  
                
                if has_doc=="on":
                    has_doc= True  
                else:
                    has_doc= False  
                question = Question(title=obj['question'],
                question_type=obj['questionType'],
                has_weight= has_weight,
                weight=obj['weight'],
                allow_doc=has_doc,
                doc_label=obj['Doclable'],
                category=category,
                )
                question.save()

                question_type =obj['questionType']
                print(question_type)
                hasOption = ["checkbox", "radio"]
                if question_type in hasOption:
                    options = obj['options']
                    for i in options:
                        newChoice = Choice.objects.create(name=i)
                        question.choice.add(newChoice.id)
                        print("The new choice name " + str(newChoice.name))
                        print("The new choice id " + str(newChoice.id))

                survey.question.add(question)
            return redirect('survey_managment:questionCreationByType', survey_id=survey_id )

   

    context = {'categories': categories,'zsurvey':zsurvey}
    return render(request, 'new_create.html', context)

def save_category(request):
    if request.method == 'POST':
        new_category_name = request.POST.get('categoryName')
        category = Category(name=new_category_name)
        category.save()

        categories = Category.objects.all()
        categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]

        return JsonResponse({'success': True, 'categories': categories_data})
    else:
        return JsonResponse({'success': False})