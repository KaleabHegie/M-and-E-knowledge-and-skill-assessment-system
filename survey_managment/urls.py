from django.urls import path
from .import views

urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.indexView, name='SurveyCreation'),
    path('login/',views.loginView, name='login'),
]
