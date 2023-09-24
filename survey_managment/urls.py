from django.urls import path
from .import views

urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.surveyCreationView, name='SurveyCreation'),
    path('change_password/' , views.change_password ,  name = 'change_password'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('ChartAnalysis/',views.Mychartanalysis, name='ChartAnalysis'),
    

]
