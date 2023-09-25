from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.indexView, name='Index'),
    path('surveyCreation/',views.surveyCreationView, name='SurveyCreation'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('ChartAnalysis/',views.Mychartanalysis, name='ChartAnalysis'),
    path('change_password', views.change_password,name='change_password')
    

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
