from django.db import models
from django.contrib.auth.models import AbstractUser 

class Line_ministry(models.Model):
    name = models.CharField( max_length=50 ,null=True)
    
    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
       
    ROLE_CHOICES = (
        ('MoPDHead', 'MoPD Head'),
        ('LineMinisterHead', 'Line Minister Head'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    phone_number = models.CharField( max_length=50 ,null=True)    
    image = models.ImageField(upload_to='',null=True)
    gender = models.CharField(max_length=1,null=True)  
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False , null=True)
    Department = models.CharField( max_length=50 ,null=True)
    Line_ministry = models.ForeignKey("Line_ministry",on_delete=models.CASCADE,null=True,blank=True)
    
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']   


