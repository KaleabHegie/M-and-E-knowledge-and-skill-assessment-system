from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth

from django.contrib.auth.models import User
from . models import *
from .forms import UserProfileForm
from django.contrib.auth import settings

# Create your views here.
def register_view(request):
	ministry = Line_ministry.objects.all()
	if request.method == 'POST':
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		email = request.POST.get('email')
		DoB= request.POST.get('dob')
		password = request.POST.get('password')
		re_password = request.POST.get('re_password')
		phone_num = request.POST.get('phone_num')
		role = request.POST.get('role')
		department = request.POST.get('department')
		line_ministry_name = request.POST.get('line_ministry_name')
		selected_gender = request.POST.get('gender')



		if password == re_password:
			if CustomUser.objects.filter(username=username).exists():
					messages.error(request , 'User Name Already Taken')
					return HttpResponse('User Name Already Taken')
			else:
				if CustomUser.objects.filter(email=email).exists():
					messages.error(request , 'Email Name Already Exits ')
					return HttpResponse('Email Name Already Exits')
				else:
					custom_user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name = first_name,last_name=last_name,
												  phone_number=phone_num, date_of_birth=DoB,Role = role, Department = department,Line_ministry =line_ministry_name ,gender= selected_gender)
					
					custom_user.save()
					
					messages.success(request,'User registered Sucessfully')
					return HttpResponse("User Registered")
		else:
			messages.error(request , 'Password Doest Not Match')
			return HttpResponse('Password does not match')

	else: 
		return render(request,'./userRegistration.html' ,{'ministry':ministry})


def login_view(request):
	user = CustomUser.objects.all()
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username , password=password)
		if user is not None: 
			auth.login(request,user)
			messages.success(request,'You Are Now LoggedIn')
			return HttpResponse('Logged in')
		elif CustomUser.objects.filter(username=username).exists():
			return HttpResponse("Incorrcet password")
		else:
			messages.error(request,'Invalid Credentials')
			return HttpResponse("Invalid User")
	else:
		return render(request,'./login.html')

def logout(request):
        auth.logout(request)
        return redirect('/greetingpage')



from .models import CustomUser

def view_profile(request):
    # Retrieve the custom user object
    custom_user = request.user
    
    # Pass the custom user object to the template
    return render(request, './profile.html', {'custom_user': custom_user})

# def edit_profile(request):
#     return render(request , './edit_profile.html' )

from .forms import UserProfileForm

def edit_profile(request):
    user = request.user
    profile = CustomUser.objects.get(username=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse('updated')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form,'user':user})


def forgotPasswordView(request):
    return render(request, 'forgot-password.html')

def user_profile(request):
    return render(request , 'profile.html' )

def users(request):
	users = CustomUser.objects.all()

	context ={
		'users':users
	}
	return render(request, 'user.html', context )
def change_password(request):
    return render(request , 'password_change.html' )


