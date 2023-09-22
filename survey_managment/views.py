from django.shortcuts import render

# Create your views here.

def indexView (request):
    return render(request, 'index.html', {})

def surveyCreationView (request):
    return render(request, 'surveyCreation.html', {})

def user_profile(request):
    return render(request , 'profile.html' )
def change_password(request):
    return render(request , 'change_password.html' )
