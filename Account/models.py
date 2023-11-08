from django.db import models
from django.contrib.auth.models import AbstractUser 

class Line_ministry(models.Model):
    name = models.CharField( max_length=50 ,null=True)
    
    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    is_MoPDHead = models.BooleanField(default=False)
    is_LineMinisterHead = models.BooleanField(default=False)
    is_LineMinisterStaff = models.BooleanField(default=False)
    phone_number = models.CharField( max_length=50 ,null=True)    
    image = models.ImageField(upload_to='',null=True)

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)  
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False , null=True)
    Role =models.CharField( max_length=50 ,null=True)
    Department = models.CharField( max_length=50 ,null=True)
    Line_ministry = models.ForeignKey("Line_ministry",on_delete=models.CASCADE,null=True)
    
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']   


