from django.db import models

# on_delete defines what to do with the current table if the foreign key is deleted

class SurveyTable(models.Model):
    # Primary Key
    surveyID = models.AutoField(primary_key=True, unique=True)
    
    # Fields/Attributes
    qualtricsSurveyID = models.CharField(max_length=30)
    releaseDate = models.DateField()
    accessedDate = models.DateField(null=True,blank=True)
       
    def __str__(self):
        return f"id: {self.surveyID} surveyID: {self.qualtricsSurveyID} date: {self.releaseDate}"
    
            
class QuestionTable(models.Model):
    # Primary Key
    questionID = models.AutoField(primary_key=True, unique=True)
    
    # Foreign Keys
    surveyID = models.ForeignKey(SurveyTable,on_delete=models.CASCADE)
    
    # Fields/Attributes
    questionType = models.CharField(max_length=30) # Mutliple choice, Rank Order, Slider, True/False, Open Text
    questionName = models.CharField(max_length=30) # This is a name attached to a question by Qualtrics
    questionTextEnglish = models.TextField()
    questionTextFrench = models.TextField()  
    
    def __str__(self):
        return f"Question: \n name: {self.questionName} \n type: {self.questionType} \n text: {self.questionTextEnglish} "   
    
class ChoiceTable(models.Model):
    # Primary Key
    choiceID = models.AutoField(primary_key=True, unique=True)
    
    # Foreign Keys
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    
    # Fields/Attributes
    recode = models.IntegerField()
    choiceTextEnglish = models.TextField()
    choiceTextFrench = models.TextField()  
    
    def __str__(self):
        return f"choice: choiceText: {self.choiceTextEnglish} recode: {self.recode}" 
    
    
class UserTable(models.Model):
    # Primary Key
    userID = models.AutoField(primary_key=True, unique=True)
    
    # Fields/Attributes
    externalDataReference = models.CharField(max_length=15)
    province = models.CharField(max_length=2)   # BC,AB,SK,MB,ON,QC,NB,NS,NL,PI,YK,NV,NW
    size = models.CharField(max_length=6)       # small, medium, large
    domain = models.CharField(max_length=30)
    languagePreference = models.CharField(max_length=2)   #EN, FR

class UserResponseTable(models.Model):
    # Primary Key
    responseID = models.AutoField(primary_key=True, unique=True)
    
    # Foreign Keys
    userID = models.ForeignKey(UserTable, on_delete=models.DO_NOTHING)
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    
    # this foriegn key might be redundant since we can access the choice through the question
    choiceID = models.ForeignKey(ChoiceTable, on_delete=models.CASCADE,null=True,blank=True)
    
    # Fields/Attributes
    answerText = models.TextField(null=True)
    answerValue = models.TextField(null=True)
    
    def __str__(self):
        if self.choiceID != None:
            return f"UserRespoinse: \nuserID: {self.userID.userID} \nrecode: {self.choiceID.recode} \nanswerText: {self.answerText} \nanswerValue: {self.answerValue}" 
        else:
            return f"UserRespoinse: \nuserID: {self.userID.userID} \nanswerText: {self.answerText} \n" 