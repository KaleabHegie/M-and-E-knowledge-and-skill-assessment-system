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
			if User.objects.filter(username=username).exists():
					messages.error(request , 'User Name Already Taken')
					return redirect('register_view')
			else:
				if User.objects.filter(email=email).exists():
					messages.error(request , 'Email Name Already Exits ')
					return redirect('register_view')
				else:
					custom_user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name = first_name,last_name=last_name)
					custom_user.save()
					system_user = System_User.objects.create(phone_number=phone_num, image=profile_picture, custom_user=custom_user,date_of_birth=DoB)
					system_user.save()
					messages.success(request,'User registered Sucessfully')
					return HttpResponse("User Registered")
		else:
			messages.error(request , 'Password Doest Not Match')
			return redirect('register_view')

	else:
		return render(request,'survey_managment/userRegistration.html')


# def login_view(request):
# 	user = User.objects.all()
# 	if request.method == 'POST':
# 		username = request.POST['username']
# 		password = request.POST['password']

# 		user = auth.authenticate(username=username , password=password)
# 		if user is not None and user.is_superuser: 
# 			auth.login(request,user)
# 			messages.success(request,'You Are Now LoggedIn')
# 			return render(request,'./dashboard/profile.html')
# 		elif user is not None:
# 						return HttpResponse("Logged in as Customer")

# 		else:
# 			messages.error(request,'Invalid Credentials')
# 			return HttpResponse("Invalid User")

		
# 	else:
# 		return render(request,'./accounts/auth-login.html')

# from django.contrib.auth import logout
# from django.shortcuts import redirect

# def logout_view(request):
#     logout(request)
#     return  redirect('pages:index')


# # def dashborad(request):
# # 	user_contact = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
# # 	return render(request,'accounts/dashborad.html',{'contacts' : user_contact})

