from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'survey_managment'


urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.surveyCreationView, name='SurveyCreation'),
    # path('user_registration/', views.user_registration,name='user_registration'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),

    path('ChartAnalysis/',views.Mychartanalysis, name='ChartAnalysis'),
    path('change_password/', views.change_password,name='change_password'),
    path('forgotPassword/', views.forgotPasswordView,name='forgotPassword'),
    # path('login/', views.loginView, name='login'),
    path('questionnaires/', views.questionnaireView, name='questionnaires'),
    path('questionnaireDetail/', views.questionnaireDetailView, name='questionnaireDetail'),
    path('createForm/', views.createForm, name='createForm'),


    # path('AllForm/', views.FormsView, name='AllForm'),
    # path('formDetail/', views.formDetailView, name='formDetail'),
    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuesion/', views.displayQuesion, name='displayQuesion'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
