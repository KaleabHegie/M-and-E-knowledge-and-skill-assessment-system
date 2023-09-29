from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth

from django.contrib.auth.models import User
from . models import *


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


		if password == re_password:
			if CustomUser.objects.filter(username=username).exists():
					messages.error(request , 'User Name Already Taken')
					return HttpResponse('User Name Already Taken')
			else:
				if CustomUser.objects.filter(email=email).exists():
					messages.error(request , 'Email Name Already Exits ')
					return HttpResponse('Email Name Already Exits')
				else:
					custom_user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name = first_name,last_name=last_name,phone_number=phone_num, image=profile_picture,date_of_birth=DoB)
					custom_user.save()
					
					messages.success(request,'User registered Sucessfully')
					return HttpResponse("User Registered")
		else:
			messages.error(request , 'Password Doest Not Match')
			return HttpResponse('Password does not match')

	else:
		return render(request,'survey_managment/templates/userRegistration.html')


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

		else:
			messages.error(request,'Invalid Credentials')
			return HttpResponse("Invalid User")

		
	else:
		return render(request,'survey_managment/templates/login.html')

# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def logout_view(request):
#     logout(request)
#     return  redirect('pages:index')


# # def dashborad(request):
# # 	user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
# # 	return render(request,'accounts/dashborad.html',{'contacts' : user_contact})

