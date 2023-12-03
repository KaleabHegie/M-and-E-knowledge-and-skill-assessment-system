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
    path('questionCreationByType/', views.questionCreationByType, name='questionCreationByType'),
    path('newQuestion/<str:questionType>/<int:s_id>/', views.newQuestion, name='newQuestion'),
<<<<<<< HEAD
    path('newCategory/', views.newCategory, name='newCategory'),
=======
    path('recommendation/', views.recommendationView, name='recommendation'),
>>>>>>> ecde6227061cfac5a9ab2352868a98a3c66e139d


    path('survey/', views.survey, name='survey'),
    path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:id>/', views.displayQuestion, name='displayQuestion'),
    path('catagorizedQuestion/<int:id>/', views.catagorizedQuestion, name='catagorizedQuestion'),
    path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),
    path('questionCreationByType/<int:survey_id>/', views.questionCreationByType, name='questionCreationByType'),
    path('survey/', views.survey, name='survey'),
    path("pending_response/",views.pending_response,name ='pending_response'),
    path('survey_detail/<int:id>', views.survey_detail, name='survey_detail'),
    path('user_response_list/<int:id>', views.user_response_list, name='user_response_list'),
    path('user_response/<int:id>/<int:response_id>', views.user_response, name='user_response'),
    path('user_response_change_status/<int:id>/<int:response_id>', views.user_response_change_status, name='user_response_change_status'),
    # path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:survey_id>/', views.displayQuestion, name='displayQuestion'),
    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),
    path('get_json/',views.get_data,name='get_data'),
   
    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),   
    path('greetingpage/',views.greetingpage_view, name='greetingpage'),
    path('surveylists/',views.survey_listss_views, name='surveylists'),
    path('user_info/',views.user_info, name='user_info'),
    path('surveylistsAnonymous/<int:user_response_id>',views.anonymous_survey_listss_views, name='anonymous_survey_listss_views'),
    path('questionForSurvey/<int:id>' , views.questionForSurvey , name = 'questionForSurvey'),
    path('questionForSurveyAnonymous/<int:id>/<int:user_response_id>' , views.questionForSurveyAnonymous , name = 'questionForSurveyAnonymous'),
    path('un_approved_survey_list/' , views.un_approved_survey_list , name = 'un_approved_survey_list'),
    path('un_approved_survey/<int:id>' , views.un_approved_survey , name = 'un_approved_survey'),
    path("load_survey/",views.load_survey,name ='load_survey'),
    path("load_ministry/",views.load_ministry,name ='load_ministry')



]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
