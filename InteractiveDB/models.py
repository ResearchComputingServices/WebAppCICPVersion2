from django.db import models

# on_delete defines what to do with the current table if the foreign key is deleted

class SurveyTable(models.Model):
    surveyID = models.IntegerField(primary_key=True)
    qualtricsSurveyID = models.CharField(max_length=30)
    date = models.DateField()
    
class QuestionContainerTable(models.Model):
    questionContainerId = models.IntegerField(primary_key=True)
    surveyID = models.ForeignKey(SurveyTable,on_delete=models.CASCADE)
    questionType = models.CharField(max_length=30) # Mutliple choice, Rank Order, Slider, True/False, Open Text
    questionName = models.CharField(max_length=30) # This is a name attached to a question by Qualtrics

class QuestionTable(models.Model):
    questionID = models.IntegerField(primary_key=True)
    questionContainerID = models.ForeignKey(QuestionContainerTable, on_delete=models.CASCADE)
    questionTextEnglish = models.TextField()
    questionTextFrench = models.TextField()        
    
class UserTable(models.Model):
    serID = models.IntegerField(primary_key=True)
    externalDataReference = models.IntegerField()
    province = models.CharField(max_length=2)   # BC,AB,SK,MB,ON,QC,NB,NS,NL,PI,YK,NV,NW
    size = models.CharField(max_length=6)       # small, medium, large
    domain = models.CharField(max_length=30)

class UserResponseTable(models.Model):
    responseID = models.IntegerField(primary_key=True)
    userID = models.ForeignKey(UserTable, on_delete=models.DO_NOTHING)
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    answerTextEnglish = models.TextField()
    answerTextFrench = models.TextField()