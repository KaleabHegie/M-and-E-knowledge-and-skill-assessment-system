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



@login_required
def new_page(request):
    return render(request,'new_create.html')

@login_required
def indexView(request):
    survey_id = request.GET.get('survey_id')
    if survey_id:
        survey = get_object_or_404(Section, id=survey_id)
        survey = get_object_or_404(Section, id=survey_id)
        questionnaires = survey.question_set.all()
        context = {
            'survey': survey,
            'questionnaires': questionnaires,
        }
        return render(request, 'index.html', context)
   
    else:
        surveys = Section.objects.all()
        surveyType = SurveyType.objects.all()
        surveys_count = Section.objects.all().count()
        questions = Question.objects.all().count()
        Response = UserResponse.objects.all().count()
        line_ministry = Line_ministry.objects.all()
        survey_years = Section.objects.order_by('created_at__year').values('created_at__year').distinct() 
        form = AnalysisForm()
       
   



        context = {'surveys_count': surveys_count, 'questions': questions, 'Response':Response , 'surveys':surveys ,
             'line_ministry':line_ministry,'form':form,'surveyType':surveyType,'survey_years':survey_years}
      
        return render(request, 'index.html', context)

@login_required
def ministries(request):
    
    return render(request , 'ministries.html')

@login_required
def filter(request):
    survey_id = request.GET.get('survey_id')
    if survey_id:
        survey = get_object_or_404(Section, id=survey_id)
        questionnaires = survey.question_set.all()
        context = {
            'survey': survey,
            'questionnaires': questionnaires,
        }
        return render(request, 'index.html', context)
   
    else:
        surveys = Section.objects.all()
        surveyType = SurveyType.objects.all()
        surveys_count = Section.objects.all().count()
        questions = Question.objects.all().count()
        Response = UserResponse.objects.all().count()
        line_ministry = Line_ministry.objects.all()
        survey_years = Section.objects.order_by('created_at__year').values('created_at__year').distinct() 
        form = AnalysisForm()
       
        



        context = {'surveys_count': surveys_count, 'questions': questions, 'Response':Response , 'surveys':surveys ,
             'line_ministry':line_ministry,'form':form,'surveyType':surveyType,'survey_years':survey_years}
      
        return render(request, 'filter.html', context)
    
@login_required
def average(request):
    return render(request , 'averages.html' )

@login_required
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
    
@login_required  
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def user_profile(request):
    return render(request , 'profile.html' )

@login_required
def edit_profile(request):
    return render(request , 'edit_profile.html' )

@login_required
def users(request):
    return render(request , 'user.html' )

@login_required
def forgotPasswordView(request):
    return render(request, 'forgot-password.html')

@login_required
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

def Mychartanalysis(request):
    data={}
    return render(request,'chart_analysis.html',data)

def jsonSender(request):
    data = {
        'questions' : list(Question.objects.all().values()),
        'categories': list(Category.objects.all().values()),
        'surveys':    list(Section.objects.all().values()),
    }
    return JsonResponse(data)

@login_required
def compareDataView(request):
    line_ministry = Line_ministry.objects.all()
    survey_type = SurveyType.objects.all()
    survey = Section.objects.all()
    survey_years = Section.objects.order_by('created_at__year').values('created_at__year').distinct() 


    context = {
        'line_ministry':line_ministry,
        'survey_type': survey_type,
        'survey':survey,
        'survey_years':survey_years
    }
    return render(request, 'compare.html',context)
from django.forms.models import model_to_dict
import json
from datetime import datetime
from django.http import HttpResponse
def datetime_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

@login_required
def get_data(request):
    surveys = Assesment.objects.all()
    sections = Section.objects.all()
    assesment = Assesment.objects.all()
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    userResponse = UserResponse.objects.all()
    for response in userResponse:
        section_id = response.forsection.id if response.forsection else None
        respone_data = {
            "id": response.id,
            "forsurvey_id": section_id,
            "submitted_by_id":response.submitted_by_id ,
            "submitted_by_lineMinistry": '' ,
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

    for category in categories:
        category_data = {
            "name": category.name,
            "has_parent": category.parent is not None,
            "parent_name": category.parent.name if category.parent else None,
            "questions": list(category.question_set.values())
        }
        data3.append(category_data)

    assesment_data_list = []
    for assesment in assesment:
        assesment_data = {
            "id": assesment.id,
            "for_line_ministry": list(assesment.for_line_ministry.values_list('id', flat=True)),
            "start_at": assesment.start_at,
            "end_at": assesment.end_at,
            "survey_type": assesment.survey_type.id if assesment.survey_type else None,
            "name": assesment.name,
            "created_at": assesment.created_at,
            "section": list(assesment.section.values_list('id', flat=True)),
        }

        assesment_data_list.append(assesment_data)
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

        for survey in sections:
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
        'Assesment': assesment_data_list,
        'section' : list(Section.objects.values()),
        'user_response': data4,
    }
    return JsonResponse(serialized_data , safe=False)


@login_required
def survey(request):
    data = {
        'surveys_employee': Assesment.objects.filter(survey_type__name = "For Employee"),
        'surveys_org': Assesment.objects.filter(survey_type__name ="For Organization"),
        }
    return render(request, 'survey.html', data)

@login_required
def line_ministrys(request):
    data = {
        "line_ministrys" : Line_ministry.objects.all()
    }
    return render(request , 'line_ministrys.html' , data)

@login_required
def line_ministry_detail(request , id):
    line_ministry = Line_ministry.objects.get(id = id)
    minister = CustomUser.objects.get(Line_ministry=line_ministry) 
    data = {
        "survey" : Section.objects.filter(assesment = id),
        "user_responses" : UserResponse.objects.filter(submitted_by = minister ),
        "line_ministry":line_ministry
    }
    return render(request , 'line_ministry_detail.html' , data)

@login_required
def user_response_list(request, id):
    survey = get_object_or_404(Section, id=id)
    user_responses = UserResponse.objects.filter(forsection=survey)
    data = {
        'survey_id': id,
        'survey': survey,
        'user_responses': user_responses,
    }
    return render(request, 'user_response_list.html', data)

@login_required
def user_response(request, id, response_id):
    survey = get_object_or_404(Section, id=id)
    user_responses = UserResponse.objects.filter(id=response_id)
    answers = Answer.objects.filter(response__in=user_responses)
    documents = Document.objects.all()  

    documents_by_answer = {}  # Dictionary to store documents for each answer
    for answer in answers:
        documents = Document.objects.filter(foranswer=answer)
        documents_by_answer[answer.id] = documents

    print(documents_by_answer)

    if request.method == 'POST':
     if 'approve' in request.POST:  
        survey = get_object_or_404(Section, id=id)
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
        survey = get_object_or_404(Section, id=id)
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
        'documents_by_answer': documents_by_answer,
        'user_responses': user_responses,
        'answers': answers,
        'documents': documents,
        'response_id': response_id
    }
    return render(request, 'user_response.html', data)

@login_required
def survey_detail(request, id):
    survey = get_object_or_404(Section, id=id)
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
    data = {
        'survey_id': id,
        'survey': Section.objects.get(id=id),
        'cat_list':cat_list,
        'user_responses': UserResponse.objects.filter(forsection_id=id),
        'questions': Section.objects.get(id=id).question.all(),
        'line_ministries' : Section.objects.get(id=id)
    }
    return render(request, 'survey_detail.html', data)

@login_required
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

@login_required
def chooseSurvey(request , id , choose_id ):
    data = {
        'choose_id':choose_id,
        'survey_id':id,
        'surveys': Section.objects.all(),
        }
    return render(request, 'chooseSurvey.html' , data)

@login_required
def displayQuestion(request, id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        survey = get_object_or_404(Section, id=id)
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
            'surveys': Section.objects.get(id=id),
            'categories': Category.objects.all(),
            'id' : id,
        }

    return render(request, 'displayQuesion.html', data)

@login_required
def catagorizedQuestion(request, id):
    if request.method == 'POST':
        selected_questions = request.POST.getlist('selected_questions')
        survey = get_object_or_404(Section, id=id)
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
            'surveys': Section.objects.get(id=id),
            'id' : id,
            'categories': Category.objects.all(),
        }

    return render(request, 'catagorizedQuestion.html', data)

@login_required
def chooseTarget(request, survey_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    survey = get_object_or_404(Section, id=survey_id)
    
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

@login_required
def questionCreationByType(request, section_id):
    survey = get_object_or_404(Section, id=section_id)
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
    zsurvey = Section.objects.get(id=section_id)
    questions = zsurvey.question.all()
    pattern = r'/newQuestion/[^/]+/\d+/'
    if request.META.get('HTTP_REFERER') and '/surveyCreation' in request.META['HTTP_REFERER']:
        messages.success(request, 'Section created successfully. Add questions to it.')  # regular expression pattern to match the URL
    if request.META.get('HTTP_REFERER') and re.search(pattern, request.META['HTTP_REFERER']):
        messages.success(request, 'Section created successfully. Add questions to it.')    
    
    return render(request, 'addQuestions.html', {'zsurvey': zsurvey, 'cat_list': cat_list})

@login_required
def newQuestion(request,questionType, s_id ):
    categories = Category.objects.prefetch_related('subcategories')
    survey = get_object_or_404(Section, id=s_id)
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

@login_required
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

@login_required
def load_survey(request):
    survey_type_id = request.GET.get("survey_type")
    survey = Section.objects.filter(survey_type_id=survey_type_id)
   
    return render(request ,"load_survey.html",{"survey":survey  })

@login_required
def pending_response(request):
    user_responses = UserResponse.objects.filter(status='pending')
    responses = UserResponse.objects.filter(status='pending').count()
    data = {
        'user_responses': user_responses,
        "responses" : responses,
    }
    return render(request , 'pendingResponse.html' , data )

@login_required
def load_ministry(request):
    survey_id = request.GET.get("survey")
    survey = Section.objects.filter(id=survey_id).first()
    line_ministries = survey.for_line_ministry.all() if survey else []
    return render(request, "load_ministry.html", {"line_ministries": line_ministries})

@login_required
def surveyCreationView(request):
    if request.method == 'POST':
        form = AssesmentForm(request.POST)
        if form.is_valid():
            survey = form.save()  
            print(survey.id)  # Check if the object has been saved to the database
            return redirect('survey_managment:sections',survey_id=survey.id )  # Pass the survey ID to the success page
        else:
            print(form.errors)  # Print any validation errors
    else:
        form = AssesmentForm()
    return render(request, 'surveyCreation.html', {'form': form})

@login_required
def sections(request , survey_id):
    assesment = Assesment.objects.get(id  = survey_id),
    data = {
        'assesment': Assesment.objects.get(id  = survey_id),
        'sections': Section.objects.filter(assesment = survey_id),
        }
    return render(request, 'Section.html', data)

@login_required
def sectionCreation(request , survey_id):
    assesment = Assesment.objects.get(id=survey_id)
    if request.method == 'POST':
        form =SectionForm(request.POST)
        if form.is_valid():
            section = form.save() 
            section.assesment.add(assesment)
            print(section.id)  # Check if the object has been saved to the database
            return redirect('survey_managment:sections', survey_id=section.id )  # Pass the survey ID to the success page
        else:
            print(form.errors)  # Print any validation errors
    else:
        form = SectionForm()
    return render(request, 'SectionCreation.html', {'form': form})

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
        'surveys_count' : Section.objects.filter(userresponse__status='recomended',  userresponse__submitted_by = user).count(),
    }
    
    return render(request, 'Final_Preview_Pages/greetingpage.html' , context)

@login_required
def survey_listss_views(request):
    
    # surveys_with_responses = [response.forsection for response in user_responses]
    # user = CustomUser.objects.get(username=user)
    # sections = Section.objects.all()
    # surveys_without_responses = sections.exclude(id__in=[survey.id for survey in surveys_with_responses])
    
   

    
    # line_ministry = user.Line_ministry
    surveys = Assesment.objects.filter( survey_type__name = "For Organization")
    for i in surveys:
       sections = Section.objects.filter(assesment = i)
       user = request.user
       user_responses = UserResponse.objects.filter(submitted_by=user)
       for j  in user_responses:
          if j.forsection == i:
           print(j)
          

    pattern = r'/questionForSurvey/\d+/'
    pattern1 = r'/questionForSurveyAnonymous/\d+/\d+/'
    if request.META.get('HTTP_REFERER') and re.search(pattern, request.META['HTTP_REFERER']):
        messages.success(request, 'Your Survey  is submitted succussesfuly.') 
        print("hello") # regular expression pattern to match the URL
    elif request.META.get('HTTP_REFERER') and re.search(pattern1, request.META['HTTP_REFERER']):
        messages.success(request, 'Your Survey is submitted succussesfuly.')    
    

    data = {
        'surveys': surveys,
        # "surveys_with_responses" : surveys_with_responses
    }
    return render(request, 'Final_Preview_Pages/SL.html', data)

@login_required
def section_list(request , survey_id):
    user = request.user
    user_responses = UserResponse.objects.filter(submitted_by=user)
    surveys_with_responses = [response.forsection for response in user_responses]


    user = CustomUser.objects.get(username=user)
    sections = Section.objects.filter(assesment = survey_id)
    surveys_without_responses = sections.exclude(id__in=[survey.id for survey in surveys_with_responses])

    data = {
        "survey_id" : survey_id,
        'sections': sections,
        "surveys_with_responses" : surveys_with_responses
    }
    return render(request, 'Final_Preview_Pages/SectionList.html', data)

@login_required
def questionForSurvey(request, id):
    survey = get_object_or_404(Section, id=id)
    questions = survey.question.all()
    cat_list = []

    for cat in Category.objects.all():
        question_filtered = survey.question.filter(category=cat)
        questions_list = [question.title for question in question_filtered]
        cat_list.append({"category": cat.name, "questions": questions_list})

    question_cat_none = survey.question.filter(category=None)
    if question_cat_none.exists():
        questions_list = [question.title for question in question_cat_none]
        cat_list.append({"category": 'No category', "questions": questions_list})

    if request.method == 'POST':
        user_response_form = UserResponseForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(question.id)) for question in survey.question.all()]
        document_forms = [DocumentForm(request.POST, request.FILES, prefix=str(question.id)) for question in survey.question.all()]
        userresponse = UserResponse.objects.create(forsection = survey , submitted_by = request.user)
        for category in cat_list:
            for question_title in category['questions']:
              if question_title.question_type ==  'checkbox' or question_title.question_type ==  'radio':
                question = Question.objects.get(id=question_title.id)
                answer_text = request.POST.getlist(f'choice_{question.id}')
                print(answer_text)
                if (len(answer_text)>0):
                  answer_string = ','.join(answer_text)
                  answer = Answer.objects.create(response=userresponse, forquestion=question, answertext=answer_string)
              else: 
                question = Question.objects.get(id=question_title.id)
                answer_text = request.POST.get(f'answer_{question.id}')
                answer = Answer.objects.create(response=userresponse, forquestion=question, answertext=answer_text)
                file = request.POST.get(f'file_{question.id}')   
                if file:
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
def recomended_survey_list(request , survey_id):
    today = date.today()
    user = request.user 
    user = CustomUser.objects.get(username = user)
    line_ministry = request.user.Line_ministry
    print(user)
    print(line_ministry)
    data = {
        "survey_id" : survey_id,
        "surveys" : Section.objects.filter(userresponse__status='recomended', assesment = survey_id , userresponse__submitted_by = user)
        }
    return render(request, 'recomended_survey_list.html', data)

@login_required
def recomended_survey(request, id):
    survey = get_object_or_404(Section, id=id)
    survey_id = Assesment.objects.get(section = id).id
    user = request.user
    response = get_object_or_404(UserResponse, forsection=survey, submitted_by=user)

    questions = Question.objects.filter(section=survey)
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
        return redirect ("survey_managment:recomended_survey_list" , survey_id=survey_id)   

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

def anonymous_survey_listss_views(request, user_response_id):
    today = date.today()
    survey_type = SurveyType.objects.get(name='For Employee')
    user_response = UserResponse.objects.get(id=user_response_id)
    line_ministry = user_response.line_ministry

    # Exclude surveys with any user responses
    surveys = Assesment.objects.filter(survey_type=survey_type, for_line_ministry=line_ministry ) \

    data = {
        'surveys': surveys,
        'user_response_id': user_response_id
    }
    return render(request, 'Final_Preview_Pages/SL_Anonymous.html', data)

def section_list_anonymous(request , survey_id , user_response_id):

    sections = Section.objects.filter(assesment = survey_id)
   
    data = {
        
        "survey_id" : survey_id,
        'sections': sections,
        "user_response_id" : user_response_id
        
    }
    return render(request, 'Final_Preview_Pages/section_list_anunymous.html', data)

def questionForSurveyAnonymous(request, id , user_response_id):
    survey = get_object_or_404(Section, id=id)
    assesment = Assesment.objects.get(section = survey).id
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
    user_response = UserResponse.objects.get(id=user_response_id)
    if request.method == 'POST':
        # value = request.POST.get('answer_16')
        # print(value)

        if user_response.forsection :
           user_response = UserResponse.objects.create(
           forsection=survey,
           department=user_response.department,
           age=user_response.age,
           line_ministry =  user_response.line_ministry ,
           year_of_experiance = user_response.year_of_experiance,
           status='approved',
    )

           user_response.save() 
           for category in cat_list:
             for i in category['questions']:
               if i.question_type ==  'checkbox' or i.question_type ==  'radio':
                question = Question.objects.get(id=i.id)
                answer_text = request.POST.getlist(f'choice_{question.id}')
                print(answer_text)
                if (len(answer_text)>0):
                  answer_string = ','.join(answer_text)
                  answer = Answer.objects.create(response=user_response, forquestion=question, answertext=answer_string)
               else: 
                question = Question.objects.get(id=i.id)
                answer_text = request.POST.get(f'answer_{question.id}')
                answer = Answer.objects.create(response=user_response, forquestion=question, answertext=answer_text)
                file = request.POST.get(f'file_{question.id}')   
                if file:
                   document = Document(foranswer=answer, document=file)       
                   document.save() 
               
           
           return redirect('survey_managment:section_list_anonymous' , survey_id=assesment , user_response_id=user_response_id)
        else :
           user_response.status = 'approved'
           user_response.forsection = survey
           user_response.save() 
           for category in cat_list:
            for i in category['questions']:
               if i.question_type ==  'checkbox' or i.question_type ==  'radio':
                question = Question.objects.get(id=i.id)
                answer_text = request.POST.getlist(f'choice_{question.id}')
                print(answer_text)
                if (len(answer_text)>0):
                  answer_string = ','.join(answer_text)
                  answer = Answer.objects.create(response=user_response, forquestion=question, answertext=answer_string)
               else: 
                question = Question.objects.get(id=i.id)
                answer_text = request.POST.get(f'answer_{question.id}')
                answer = Answer.objects.create(response=user_response, forquestion=question, answertext=answer_text)
                file = request.POST.get(f'file_{question.id}')   
                if file:
                   document = Document(foranswer=answer, document=file)       
                   document.save() 
          
           return redirect('survey_managment:section_list_anonymous' , survey_id=assesment , user_response_id=user_response_id)
    else:
        anonymous_user_response_form = AnonymousUserResponseForm()
        answer_forms = [AnswerForm(prefix=str(question.id)) for question in survey.question.all()]

    context = {
        'survey': survey,
        'cat_list': cat_list,
        'questions': questions,
        'anonymous_user_response_form': anonymous_user_response_form,
        'answer_forms': answer_forms,
    }

    return render(request, 'Final_Preview_Pages/surveyForAnonymous.html', context)

def createQuestion(request,survey_id ):
    zsurvey = Section.objects.get(id=survey_id)
    categories = Category.objects.all()
    survey = get_object_or_404(Section, id=survey_id)
    if request.method == 'POST':
            objects_json = request.POST.get('objects')
            objects = json.loads(objects_json)
            print(objects)
            for obj in objects:
                category_id = obj['category']
                category = None if category_id == '' else get_object_or_404(Category ,id=category_id)
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
                allow_doc=has_doc,
                )
                weight = obj['weight']
                doc_label=obj['Doclable']
                category = category
                if weight or doc_label or category :
                    try:
                        question.weight = float(weight)
                        question.doc_label = doc_label
                        question.category = category
                    except ValueError:
                        pass
                else:
                    question.weight = None
                    question.doc_label = None
                    question.category = None
                    
                question.save()

                question_type =obj['questionType']
               
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

   

    context = {'categories': categories,'zsurvey':zsurvey ,'type_field_choices': TYPE_FIELD}
    return render(request, 'new_create.html', context)

def save_category(request):
    if request.method == 'POST':
        new_category_name = request.POST.get('categoryName')
        parent_id= request.POST.get('parentId')
        print(parent_id)
        # Check if a category with the same name already exists
        existing_category = Category.objects.filter(name=new_category_name).first()

        if existing_category:
            # Category with the same name already exists, return a failure response
            return JsonResponse({'success': False, 'message': 'Category already exists.'})
            

        if parent_id:
            parent_category = get_object_or_404(Category, id=parent_id)
            category = Category(name=new_category_name,parent=parent_category)
        else:
            category = Category(name=new_category_name, parent=None)
        category.save()

        categories = Category.objects.all()
        categories_data = [{'id': cat.id, 'name': cat.name} for cat in categories]
        print(categories_data)
        return JsonResponse({'success': True, 'categories': categories_data})
    else:
        return JsonResponse({'success': False})    