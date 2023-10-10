from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)

admin.site.register(Questionnaire)

admin.site.register(Survey)

admin.site.register(Catagory)

admin.site.register(Choice)

admin.site.register(Choice_group)

