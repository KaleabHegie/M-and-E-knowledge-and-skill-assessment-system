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
    path('newForm/', views.newForm, name='newForm'),
    path('questionCreationByType/', views.questionCreationByType, name='questionCreationByType'),
    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/<int:id>/', views.chooseSurvey, name='chooseSurvey'),
    path('questionnaire/<int:questionnaire_id>/', views.display_questionnaire, name='display_questionnaire'),
    path('displayQuestion/<int:survey_id>/<int:questionnaire_id>/', views.displayQuestion, name='displayQuestion'),
    path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),


    path('surveydisplay/', views.skill_assessment_survey_view, name="surveydisplay"),
    path('surveydisplay/<int:category_id>/Catagory_list/', views.skill_assessment_survey_view, name="surveydisplay"),

    path('surveydisplay/<int:question_id>/answer/', views.answer_question, name='answer_question'),
    # path('category-questions/', views.category_questions, name='category_questions'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
