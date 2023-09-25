from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth

from django.contrib.auth.models import User
from . models import *


# Create your views here.
def register_view(request):
	if request.method == 'POST':
		full_name = request.POST['First']
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password == password2:
			if User.objects.filter(username=username).exists():
					messages.error(request , 'User Name Already Taken')
					return redirect('accounts:register_view')
			else:
				if User.objects.filter(email=email).exists():
					messages.error(request , 'Email Name Already Exits ')
					return redirect('accounts:register_view')
				else:
					user = User.objects.create_user(username=username,password=password,email=email,first_name=full_name)
					user.save()
					messages.success(request,'You Are Now Registered')
					return redirect('accounts:login_view')
		else:
			messages.error(request , 'Password Doest Not Match')
			return redirect('accounts:register_view')

	else:
		return render(request,'./accounts/auth-signup.html')


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

