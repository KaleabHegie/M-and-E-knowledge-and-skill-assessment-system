from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(UserResponse)
admin.site.register(Department)
admin.site.register(SurveyType)
admin.site.register(Document)


