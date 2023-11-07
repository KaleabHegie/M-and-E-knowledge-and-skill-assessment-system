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
    path('survey_questionnaire/', views.surveyQuestionnaireView, name='survey_questionnaire'),

    path('survey_questionnaire_detail/<int:survey_id>/<int:questionnaire_id>/', views.surveyQuestionnaireDetailView, name='survey_questionnaire_detail'),
    
    path('questionnaires/', views.questionnaireView, name='questionnaires'),
    path('questionnaireDetail/', views.questionnaireDetailView, name='questionnaireDetail'),
    path('newForm/', views.newForm, name='newForm'),

    path('questionCreationByType/', views.questionCreationByType, name='questionCreationByType'),
    path('newQuestion/(?P<questionType>[a-zA-Z]+)/', views.newQuestion, name='newQuestion'),
    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:id>/', views.displayQuestion, name='displayQuestion'),
    path('catagorizedQuestion/<int:id>/', views.catagorizedQuestion, name='catagorizedQuestion'),
    path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),
    path('questionCreationByType/<int:survey_id>/', views.questionCreationByType, name='questionCreationByType'),
    path('survey/', views.survey, name='survey'),
    path('survey_detail/<int:id>', views.survey_detail, name='survey_detail'),
    path('user_response/<int:id>', views.user_response, name='user_response'),
    # path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:survey_id>/', views.displayQuestion, name='displayQuestion'),
    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),

   
    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),   
    path('greetingpage/',views.greetingpage_view, name='greetingpage'),
    path('surveys/', views.surveyss_view, name ='surveys'),
    path('surveylists/<int:id>',views.survey_listss_views, name='surveylists'),
    path('questionForSurvey/<int:id>' , views.questionForSurvey , name = 'questionForSurvey')


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
