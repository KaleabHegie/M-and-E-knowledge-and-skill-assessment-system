from django.urls import path
from .import views

urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.indexView, name='SurveyCreation'),
    path('user_profile/',views.user_profile, name='user_profile'),
    

]
