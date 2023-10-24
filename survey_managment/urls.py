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

    path('compareData/', views.compareDataView, name='compareData'),
    path('survey_questionnaire/<int:id>/', views.surveyQuestionnaireView, name='survey_questionnaire'),

    path('survey_questionnaire_detail/<int:survey_id>/<int:questionnaire_id>/', views.surveyQuestionnaireDetailView, name='survey_questionnaire_detail'),
    
    path('questionnaires/', views.questionnaireView, name='questionnaires'),
    path('questionnaireDetail/', views.questionnaireDetailView, name='questionnaireDetail'),
    path('newForm/', views.newForm, name='newForm'),

    path('questionCreationByType/', views.questionCreationByType, name='questionCreationByType'),
    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:id>/', views.displayQuestion, name='displayQuestion'),
    path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),

    path('questionCreationByType/<int:survey_id>/', views.questionCreationByType, name='questionCreationByType'),
    path('survey/', views.survey, name='survey'),
    # path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:survey_id>/', views.displayQuestion, name='displayQuestion'),
    path('jsonSender/<int:id>' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),



   
    path('greetingpage/',views.greetingpage_view, name='greetingpage'),
    path('userinfo/',views.userinfo_view, name='userinfo'),
    path('skillassesmentpage/',views.skill_ass_sur_view,  name='skillassesmentpage'),
    path('lineminsurpage/',views.line_min_sur_view, name='lineminsurpage'),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
