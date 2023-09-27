from django.db import models
from django.contrib.auth.models import AbstractUser 



class CustomUser(AbstractUser):
    is_MoPDHead = models.BooleanField(default=False)
    is_LineMinisterHead = models.BooleanField(default=False)
    is_LineMinisterStaff = models.BooleanField(default=False)
    phone_number = models.CharField( max_length=50 ,null=True)    
    image = models.ImageField(upload_to='',null=True)
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False , null=True)
    
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']   

    
