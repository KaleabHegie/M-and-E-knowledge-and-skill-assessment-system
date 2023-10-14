from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'Account'

urlpatterns = [
    path('register/',views.register_view, name='register_view'),
    path('Login/',views.login_view, name='Login'),
    path('view_profile/',views.view_profile, name='view_profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('users/',views.users, name='users'),
    path('change_password/', views.change_password,name='change_password'),
    path('forgotPassword/', views.forgotPasswordView,name='forgotPassword'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
