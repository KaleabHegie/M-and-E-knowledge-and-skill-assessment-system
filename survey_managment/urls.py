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
    path('questionCreationByType/<int:section_id>/', views.questionCreationByType, name='questionCreationByType'),
     path('sections/<int:survey_id>/', views.sections, name='sections'),
    path('sectionCreation/<int:survey_id>/', views.sectionCreation, name='sectionCreation'),
    path('newQuestion/<str:questionType>/<int:s_id>/', views.newQuestion, name='newQuestion'),
    # path('newCategory/', views.newCategory, name='newCategory'),
    path('createQuestion/<int:survey_id>/', views.createQuestion, name='createQuestion'),
    path('save_category/' , views.save_category, name='save_category'),

    path('survey/', views.survey, name='survey'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:message_id>/reply/', views.reply_to_message, name='reply_to_message'),
    path('sent/', views.sent, name='sent'),
    path('draft/', views.draft, name='draft'),
    path('trash/', views.trash, name='trash'),
    path('compose/', views.compose, name='compose'),
    path('read/<int:id>', views.read, name='read'),
    
    path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:id>/', views.displayQuestion, name='displayQuestion'),
    path('catagorizedQuestion/<int:id>/', views.catagorizedQuestion, name='catagorizedQuestion'),
    path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),
    path('questionCreationByType/<int:survey_id>/', views.questionCreationByType, name='questionCreationByType'),
    path('QuestionCategories/', views.QuestionCategories, name='QuestionCategories'),
    path('survey/', views.survey, name='survey'),
    path('line_ministrys/', views.line_ministrys, name='line_ministrys'),
    path('line_ministrys/<int:id>', views.line_ministry_detail, name='line_ministry_detail'),
    path("pending_response/",views.pending_response,name ='pending_response'),
    path('survey_detail/<int:id>', views.survey_detail, name='survey_detail'),
    path('user_response_list/<int:id>', views.user_response_list, name='user_response_list'),
    path('user_response/<int:id>/<int:response_id>', views.user_response, name='user_response'),
    # path('chooseSurvey/<int:id>/<int:choose_id>/', views.chooseSurvey, name='chooseSurvey'),
    path('displayQuestion/<int:survey_id>/', views.displayQuestion, name='displayQuestion'),
    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),
    path('get_json/',views.get_data,name='get_data'),
    path('filter_data/',views.filter,name='filter'),
    path('average_data/',views.average,name='average'),

    path('jsonSender/' , views.jsonSender , name = 'jsonSender'),
    # path('choose-target/<int:survey_id>/<int:question_id>/', views.chooseTarget, name='chooseTarget'),   
    path('greetingpage/',views.greetingpage_view, name='greetingpage'),
    path('surveylists/',views.survey_listss_views, name='surveylists'),
    path('section_list/<int:survey_id>',views.section_list, name='section_list'),
    path('user_info/',views.user_info, name='user_info'),
    path('surveylistsAnonymous/<int:user_response_id>',views.anonymous_survey_listss_views, name='anonymous_survey_listss_views'),
    path('questionForSurvey/<int:id>' , views.questionForSurvey , name = 'questionForSurvey'),
    path('questionForSurveyAnonymous/<int:id>/<int:user_response_id>' , views.questionForSurveyAnonymous , name = 'questionForSurveyAnonymous'),
    path('recomended_survey_list/<int:survey_id>' , views.recomended_survey_list , name = 'recomended_survey_list'),
    path('recomended_survey/<int:id>' , views.recomended_survey , name = 'recomended_survey'),
    path('previous_analysis/' , views.previous_analysis , name = 'previous_analysis'),
    path("load_survey/",views.load_survey,name ='load_survey'),
    path("load_ministry/",views.load_ministry,name ='load_ministry')



]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
