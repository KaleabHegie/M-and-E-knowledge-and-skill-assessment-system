from django.db import models
from django.contrib.auth.models import AbstractUser 

class Line_ministry(models.Model):
    name = models.CharField( max_length=50 ,null=True)
    
    def __str__(self) -> str:
        return self.name

class CustomUser(AbstractUser):
    phone_number = models.CharField( max_length=50 ,null=True)    
    email = models.EmailField(unique = True)
    image = models.ImageField(upload_to='',null=True,blank=True)
    gender = models.CharField(max_length=1,null=True)  
    date_of_birth = models.DateField( auto_now=False, auto_now_add=False , null=True)
    Department = models.CharField( max_length=50 ,null=True)
    Line_ministry = models.ForeignKey("Line_ministry",on_delete=models.CASCADE,null=True,blank=True)
    is_mopd_head = models.BooleanField(null=True , blank=True)
    is_line_minister_head  = models.BooleanField(null=True , blank=True)
    is_first_time = models.BooleanField(default=True)
    REQUIRED_FIELDS = ['first_name','username','last_name']
    USERNAME_FIELD = 'email'

    
    


