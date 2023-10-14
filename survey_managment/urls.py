from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'survey_managment'


urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.surveyCreationView, name='SurveyCreation'),
    path('ChartAnalysis/',views.Mychartanalysis, name='ChartAnalysis'),
    path('change_password/', views.change_password,name='change_password'),
    path('forgotPassword/', views.forgotPasswordView,name='forgotPassword'),
    # path('login/', views.loginView, name='login'),


    path('survey_questionnaire/<int:id>/', views.surveyQuestionnaireView, name='survey_questionnaire'),

    path('survey_questionnaire_detail/<int:survey_id>/<int:questionnaire_id>/', views.surveyQuestionnaireDetailView, name='survey_questionnaire_detail'),
    
    path('questionnaires/', views.questionnaireView, name='questionnaires'),
    path('questionnaireDetail/', views.questionnaireDetailView, name='questionnaireDetail'),
    path('createForm/', views.createForm, name='createForm'),
    path('createFormTWO/<arg>/', views.createFormTWO, name='createFormTWO'),
    path('questionCreationByType/', views.questionCreationByType, name='questionCreationByType'),
    # path('textQuestion/', views.questionType, name='textQuestion'),
    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/', views.displayQuestion, name='displayQuestion'),

    path('skillassessmentsurvey/',views.skill_assessment_survey_view, name='skillassessmentsurvey'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
