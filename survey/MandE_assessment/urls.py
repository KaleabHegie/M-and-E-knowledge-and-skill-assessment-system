
from django.contrib import admin
from django.urls import path , include


from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('survey_managment.urls')) ,
    path('account/', include('Account.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

