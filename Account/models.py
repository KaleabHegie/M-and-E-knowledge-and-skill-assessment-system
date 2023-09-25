from django.db import models
from django.contrib.auth.models import AbstractUser 


class CustomUser(AbstractUser):
    is_MoPDHead = models.BooleanField(default=False)
    is_LineMinisterHead = models.BooleanField(default=False)
    is_LineMinisterStaff = models.BooleanField(default=False)
    
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']   

class System_User(models.Model):
    phone_number = models.CharField( max_length=50)    
    image = models.ImageField(upload_to='')
    custom_user = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False , null=True)