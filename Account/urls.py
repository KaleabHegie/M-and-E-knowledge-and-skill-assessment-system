from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'Account'

urlpatterns = [
    path('register/',views.register_view, name='register_view'),
    path('login/',views.login_view, name='login'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
