from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth

from django.contrib.auth.models import User
from . models import *
from .forms import UserProfileForm
from django.contrib.auth import settings

# Create your views here.
def register_view(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		email = request.POST['email']
		DoB= request.POST['dob']
		profile_picture= request.POST['profile_pic']
		password = request.POST['password']
		re_password = request.POST['re_password']
		phone_num = request.POST['phone_num']
		role = request.POST['role']
		line_ministry = request.POST['line_ministry']
		department = request.POST['department']



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
												  phone_number=phone_num, image=profile_picture,date_of_birth=DoB,Role = role, Department = department, Line_ministry =line_ministry )
					custom_user.save()
					
					messages.success(request,'User registered Sucessfully')
					return HttpResponse("User Registered")
		else:
			messages.error(request , 'Password Doest Not Match')
			return HttpResponse('Password does not match')

	else: 
		return render(request,'./userRegistration.html')


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

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return  redirect('pages:index')


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

    return render(request, 'edit_profile.html', {'form': form})


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


