from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy


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


def indexView (request):
    return render(request, 'index.html', {})

# def loginView(request):
#     return render(request, 'login.html')

def forgotPasswordView(request):
    return render(request, 'forgot-password.html')

def surveyCreationView (request):
    return render(request, 'surveyCreation.html', {})

def user_profile(request):
    return render(request , 'profile.html' )

def change_password(request):
    return render(request , 'change_password.html' )
# def user_registration(request):
#     return render(request , 'userRegistration.html' )

def Mychartanalysis(request):
    data={}
    return render(request,'chart_analysis.html',data)

def FormsView(request):
    return render(request, 'Forms.html')

def formDetailView(request):
    return render(request, 'FormDetail.html')

def survey(request):
    return render(request, 'survey.html')

def chooseSurvey(request):
    return render(request, 'chooseSurvey.html')

def displayQuesion(request):
    return render(request, 'displayQuesion.html')




