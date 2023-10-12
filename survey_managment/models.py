from django.db import models

# Create your models here.
class Survey(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

class Questionnaire(models.Model):
    name = models.CharField( max_length=100)
    instruction = models.TextField()
    created_at = models.DateTimeField( auto_now=False, auto_now_add=False)
    survey = models.ForeignKey("Survey",on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Catagory(models.Model):
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
    for_choice_group = models.ForeignKey(Choice_group, on_delete=models.CASCADE)

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
    label = models.TextField()
    question_type = models.CharField(max_length=100, choices=TYPE_FIELD)
    for_questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    choice_group = models.ForeignKey(Choice_group, on_delete=models.CASCADE ,  null=True , blank=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE ,  null=True , blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE , null=True , blank=True)
    has_weight = models.BooleanField()
    weight = models.IntegerField()
    allow_doc = models.BooleanField()
    doc_label = models.TextField(null=True)


    def __str__(self):
        return self.title



