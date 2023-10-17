from django.db import models
from Account.models import CustomUser

# Create your models here.
class Survey(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    name = models.CharField( max_length=100)
    instruction = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    survey = models.ForeignKey("Survey",on_delete=models.CASCADE,null=True,blank=True)  
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField( max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name
    
class Choice_group(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

    
class Choice(models.Model):
    name = models.TextField()
    weight = models.IntegerField()
    for_choice_group = models.ForeignKey(Choice_group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    
TYPE_FIELD = [
        ("Text" ,"Text"),
        ("Number", "Number"),
        ("Radio", "Radio"),
        ("Multi-Select", "Multi-Select"),
        ("Text-Area", "Text Area"),
        ("URL", "URL"),
        ("Email", "Email"),
        ("Date", "Date"),
        ("Rating", "Rating")
    ]
    
class Question(models.Model):
    title = models.TextField()
    label = models.TextField(null=True,blank=True)
    question_type = models.CharField(max_length=100, choices=TYPE_FIELD)
    for_questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    choice = models.ManyToManyField(Choice)
    catagory = models.ForeignKey(Category, on_delete=models.CASCADE , null=True , blank=True)
    has_weight = models.BooleanField(blank=True)
    weight = models.IntegerField(blank=True)
    allow_doc = models.BooleanField(blank=True)
    doc_label = models.TextField(null=True,blank=True)


    def __str__(self):
        return self.title



class Department(models.Model):
    department_no=models.IntegerField()
    department_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department_name

class UserResponse(models.Model):
    forsurvey = models.ForeignKey("Survey", on_delete=models.CASCADE , null=True , blank=True)
    submitted_by =models.ForeignKey("Account.CustomUser", on_delete=models.CASCADE , null=True , blank=True)
    submitted_at = models.DateTimeField(auto_now=True)
    submitted_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.submitted_by


class Answer(models.Model):
    forquestion=models.ForeignKey("Question", on_delete=models.CASCADE , null=True , blank=True)
    answertext= models.CharField(max_length=500)
    response = models.ForeignKey("UserResponse", on_delete=models.CASCADE , null=True , blank=True)

    def __str__(self) -> str:
        return self.forquestion
    


