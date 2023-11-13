from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from . models import *
from .forms import UserProfileForm
from django.contrib.auth import settings
from django.contrib.auth import logout
from survey_managment.views import survey_listss_views 


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
		line_ministry_id = request.POST.get('line_ministry')
		line_ministry = Line_ministry.objects.get(id=line_ministry_id)
		selected_gender = request.POST.get('gender')
		is_mopd_head = request.POST.get('is_mopd_head') == 'on'
		is_line_minister_head = request.POST.get('is_line_minister_head') == 'on'
		is_line_minister_staff = request.POST.get('is_line_minister_staff') == 'on'



		if password == re_password:
			if CustomUser.objects.filter(username=username).exists():
					messages.error(request , 'User Name Already Taken')
					return HttpResponse('User Name Already Taken')
			else:
				if CustomUser.objects.filter(email=email).exists():
					messages.error(request , 'Email Name Already Exits ')
					return HttpResponse('Email Name Already Exits')
				else:
					custom_user = CustomUser.objects.create_user(username=username,password=password,email=email,
												  first_name = first_name,last_name=last_name,
												  phone_number=phone_num, date_of_birth=DoB,Role = role, 
												  Department = department,Line_ministry =line_ministry ,
												  gender= selected_gender ,is_MoPDHead=is_mopd_head,
            is_LineMinisterHead=is_line_minister_head,
            is_LineMinisterStaff=is_line_minister_staff)
					
					custom_user.save()
					
					messages.success(request,'User registered Sucessfully')
					
					return redirect('Account:users')
		else:
			messages.error(request , 'Password Doest Not Match')
			return HttpResponse('Password does not match')

	else: 
		return render(request,'./userRegistration.html' ,{'ministry':ministry})


def login_view(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                auth.login(request, user)
                return redirect('survey_managment:Index')
            elif user is not None:
                auth.login(request, user)
                return redirect('survey_managment:surveylists')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('Account:Login')
           
    else:
        return render(request, 'login.html' )


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

from django.shortcuts import render, redirect
from .forms import UserProfileForm ,Admin_Update

def edit_profile(request):
    user = request.user
    profile = CustomUser.objects.get(username=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form data to the database
            instance = form.save(commit=False)
            instance.image = form.cleaned_data['image']
            instance.save()
            return redirect('Account:view_profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})



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


@login_required
def update_users(request, id):
    users = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = Admin_Update(request.POST, request.FILES, instance=users)
        if form.is_valid():
            form.save()
            return redirect('Account:users')
    else:
        form = Admin_Update(instance=users)
    return render(request, './update_users.html', {'form': form})


@login_required
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.delete()
        return redirect('Account:users')
    return render(request, 'delete_user.html', {'user': user})