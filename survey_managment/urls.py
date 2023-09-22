from django.urls import path
from .import views

urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.indexView, name='SurveyCreation'),
<<<<<<< HEAD
    path('login/',views.loginView, name='login'),
=======
    path('user_profile/',views.user_profile, name='user_profile'),
    path('change_password/',views.change_password, name='change_password'),



>>>>>>> 000d2fa8c3b24a11e61df429e32e9488f45baf53
]
