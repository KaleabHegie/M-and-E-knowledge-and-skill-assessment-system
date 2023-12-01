from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
app_name = 'Account'

urlpatterns = [
    path('register/',views.register_view, name='register_view'),
    path('Login/',views.login_view, name='Login'),
    path('logout/',views.logout, name='logout'),

    path('view_profile/',views.view_profile, name='view_profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('users/',views.users, name='users'),
    path('change_password/', views.change_password,name='change_password'),
    path('forgotPassword/', views.forgotPasswordView,name='forgotPassword'),
    path('update/<str:id>/', views.update_users, name='update_users'),
    path('delete/<str:id>/', views.delete_user, name='delete_users'),
    path('change_password' , views.change_password , name='change_password'),
     path('add_line_ministry', views.add_line_ministry, name='add_line_ministry'),



]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
