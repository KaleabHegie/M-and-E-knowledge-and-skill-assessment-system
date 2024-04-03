import re
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from . models import *
from .forms import *
from django.contrib.auth import settings
from django.contrib.auth import logout
from survey_managment.views import survey_listss_views 
from django.core.mail import send_mail
import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



# Create your views here.


def send_reg_email(request,email,first_name,last_name,password, stop_event):
    while not stop_event.is_set():
        subject, from_email, to = 'Registration Successful', 'benjiyg400@gmail.com', f"{email}"
        text_content = "Registration Successful"
        context = {
            'first_name': first_name,
            'last_name' : last_name,
            'email' : email,
            'password' : password
        }
        html_content = render_to_string('success-email.html',context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            print('Email sent')

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
    department = request.POST.get('department')
    line_ministry_id = request.POST.get('line_ministry')
    line_ministry = Line_ministry.objects.get(id=line_ministry_id)
    selected_gender = request.POST.get('gender')
    is_mopd_head = request.POST.get('is_mopd_head') == 'on'
    is_line_minister_head = request.POST.get('is_line_minister_head') == 'on'
    



    if password == re_password:
      if CustomUser.objects.filter(username=username).exists():
          messages.error(request , 'User Name Already Taken')
          return HttpResponse('User Name Already Taken')
      else:
        if CustomUser.objects.filter(email=email).exists():
          messages.error(request , 'Email Name Already Exits ')
          return HttpResponse('Email Name Already Exits ')
        elif CustomUser.objects.filter(Line_ministry=line_ministry).exists():
          messages.error(request , 'User Exists For this line ministry')
          return HttpResponse('User Exists For this line ministry')
        else:
          custom_user = CustomUser.objects.create_user(username=username,password=password,email=email,
                          first_name = first_name,last_name=last_name,
                          phone_number=phone_num, date_of_birth=DoB,
                          Department = department,Line_ministry =line_ministry ,
                          gender= selected_gender ,is_mopd_head=is_mopd_head,
            is_line_minister_head=is_line_minister_head)
          
          custom_user.save()

          stop_event = threading.Event()
          background_thread = threading.Thread(target=send_reg_email, args=(request,email,first_name,last_name,password, stop_event), daemon=True)
          # Start the background thread
          background_thread.start()
          stop_event.set()
          
          messages.success(request , 'User registered Sucessfully')
          
          return redirect('Account:users')
    else:
      messages.error(request , 'Password Doest Not Match')
      return HttpResponse('Password does not match')

  else: 
    return render(request,'./userRegistration.html' ,{'ministry':ministry})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=email, password=password)

        if user is not None and user.is_authenticated:
            # if user.is_first_time and user.is_line_minister_head:
            #     auth.login(request, user)
            #     return redirect('Account:change_password')
            if user.is_superuser:
                auth.login(request, user)
                return redirect('survey_managment:Index')
            else:
                auth.login(request, user)
                return redirect('survey_managment:surveylists')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('Account:Login')
    else:
        return render(request, 'login.html')

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
    profile = CustomUser.objects.get(email=user)
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
  context ={
    'users':CustomUser.objects.all(), 
    'ministrys' : Line_ministry.objects.all(),
    'admins' : CustomUser.objects.filter(is_mopd_head = True)
  }
  if request.META.get('HTTP_REFERER') and re.search( r'/account/update/\d+/' , request.META['HTTP_REFERER']):
        messages.success(request, 'User Successusfuly Updated')    
  return render(request, 'user.html', context )
  



@login_required
def update_users(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = Admin_Update(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('Account:users')
    else:
        form = Admin_Update(instance=user)
    return render(request, './update_users.html', {'form': form,'user':user})

@login_required
def add_line_ministry(request):
    if request.method == 'POST':
        form = LineMinistryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Account:users')  # Redirect to the line ministry list view
    else:
        form = LineMinistryForm()
    
    context = {'form': form}
    return render(request, 'add_line_ministry.html', context)

@login_required
def delete_user(request, id):
    user = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        user.delete()
    return render(request, 'delete_user.html', {'user': user})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_first_time = False
            user.save()
            return redirect('Account:Login')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, './change_password.html', {'form': form})