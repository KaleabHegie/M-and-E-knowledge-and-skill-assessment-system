from django.db import models
from Account.models import CustomUser , Line_ministry
from django.db.models import UniqueConstraint

# Create your models here.


class Assesment(models.Model):
    for_line_ministry = models.ManyToManyField( Line_ministry )
    start_at = models.DateField(null=True , auto_now=False, auto_now_add=False)
    end_at = models.DateField(null=True , auto_now=False, auto_now_add=False)
    survey_type = models.ForeignKey("SurveyType" , on_delete=models.CASCADE , null=True)
    name = models.CharField(max_length=200)
    created_at = models.DateField(auto_now=True, auto_now_add=False , null=True)
    section = models.ManyToManyField("Section")

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=200)
    instruction = models.TextField(null=True,blank=True)
    created_at = models.DateField(auto_now=True, auto_now_add=False , null=True)
    question = models.ManyToManyField("Question")
    
    def __str__(self):
        return self.name
    

    
class SurveyType(models.Model):
    name = models.CharField( max_length=50)  
    def __str__(self):
        return self.name 
    


TYPE_FIELD = [
        ("text" ,"text"),
        ("number", "number"),
        ("checkbox", "checkbox"),
        ("radio", "radio"),
        ("textarea", "textarea"),
        ("url", "url"),
        ("email", "email"),
        ("date", "date"),
        ("rating", "rating")
    ]
    
class Question(models.Model):
    title = models.TextField()
    label = models.TextField(null=True,blank=True)
    question_type = models.CharField(max_length=100, choices=TYPE_FIELD)
    choice = models.ManyToManyField("Choice"  , blank=True)
    category = models.ForeignKey("Category", on_delete=models.CASCADE , null=True , blank=True)
    has_weight = models.BooleanField(default=False)
    weight = models.IntegerField(blank=True,null=True)
    allow_doc = models.BooleanField(default = False)
    doc_label = models.TextField(null=True , blank = True)


    def __str__(self):
        return self.title
    

    
class Choice(models.Model):
    name = models.TextField()
    weight = models.IntegerField(null=True , blank=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField( max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    department_no=models.IntegerField()
    department_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department_name
        
class UserResponse(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('recomended', 'Recomended'),
    ]
    forsection = models.ForeignKey("Section", on_delete=models.CASCADE , null=True , blank=True)
    forassesment = models.ForeignKey("Assesment", on_delete=models.CASCADE , null=True , blank=True)
    submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now=True)
    year_of_experiance = models.IntegerField(null=True , blank=True)
    department = models.CharField( max_length=50 , null=True , blank=True)
    age =models.IntegerField( null=True , blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending' ,  null=True , blank=True)
    line_ministry = models.ForeignKey(Line_ministry , on_delete=models.CASCADE , null=True , blank=True)



    def __str__(self):
        return str(self.submitted_by)
    
class Answer(models.Model):
    response = models.ForeignKey("UserResponse", on_delete=models.CASCADE , null=True , blank=True)
    forquestion=models.ForeignKey("Question", on_delete=models.CASCADE , null=True , blank=True)
    answertext= models.CharField(max_length=500)
    recommendation = models.TextField(null=True, blank=True)
    def __str__(self) -> str:
        return self.answertext
    

class Document(models.Model):
    foranswer = models.ForeignKey(Answer , on_delete=models.CASCADE)    
    document = models.FileField(upload_to='') 
    
    def __str__(self) -> str:
        return self.document.name


class ContactUs(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('draft', 'Draft'),
        ('inbox', 'Inbox'),
        ('trash', 'Trash'),
    )

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES , null=True)
    read = models.BooleanField(default=False)
    

    def __str__(self):
        return self.name