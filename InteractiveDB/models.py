from django.db import models
import pandas as pd
# from djmoney.models.fields import MoneyField

# on_delete defines what to do with the current table if the foreign key is deleted

########################################################################################################################################################

class SurveyTable(models.Model):    
    # Fields/Attributes
    qualtricsSurveyID = models.CharField(max_length=30)
    releaseDate = models.DateField()
    fetchedDate = models.DateField(null=True,blank=True)
    surveyTheme = models.CharField(max_length=30)
    surveysubThemeEnglish = models.CharField(max_length=150)
    surveysubThemeFrench = models.CharField(max_length=150)
    surveyWeek = models.CharField(max_length=50)
       
    def __str__(self):
        return f"id: {self.id} surveyID: {self.qualtricsSurveyID} releaseDate: {self.releaseDate} surveyTheme: {self.surveyTheme} surveysubThemeEnglish: {self.surveysubThemeEnglish} surveysubThemeFrench: {self.surveysubThemeFrench}"
    
########################################################################################################################################################
            
class QuestionTable(models.Model):
    
    # Foreign Keys
    surveyID = models.ForeignKey(SurveyTable,on_delete=models.CASCADE)
    
    parentQuestionID = models.ForeignKey('self', 
                                         on_delete=models.CASCADE, 
                                         null=True,
                                         blank=True)
    
    # Fields/Attributes
    questionType = models.CharField(max_length=30) # Mutliple choice, Rank Order, Slider, matrix, Open Text, text/graphic
    questionName = models.CharField(max_length=30) # This is a name attached to a question by Qualtrics
   
    questionTextEnglish = models.TextField()
    questionTextFrench = models.TextField() 
   
    questionTheme = models.CharField(max_length=30)
    questionLabel = models.CharField(max_length=30)
   
    jsonKey = models.TextField() # used for matching with french survey file
   
    def __str__(self):
        return f"Question: {self.questionName} \n id: {self.id} \n type: {self.questionType} \n theme: {self.questionTheme} \n text: {self.questionTextEnglish} "   
    
    def GetDataFileEntry(self):
        
        questionKey = self.jsonKey
        questionText = self.questionTextEnglish # TODO: handle fench
        questionTheme = self.questionTheme
    
        df = pd.DataFrame({ 'QuestionKey' : questionKey,
                            'QuestionText' : questionText,
                            'QuestionTheme' : questionTheme,                  
                      
                            }, index=[0])

        return df
    
    def GetDataFileString(self):
       questionKey = self.jsonKey
       questionText = self.questionTextEnglish # TODO: handle fench
       questionTheme = self.questionTheme 
       
       dataString = questionKey +','+questionText+','+questionTheme
       
       return dataString
    
########################################################################################################################################################
    
class ChoiceTable(models.Model):
    
    # Foreign Keys
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    
    # Fields/Attributes
    recode = models.IntegerField()
    choiceTextEnglish = models.TextField(null=True, blank=True)
    choiceTextFrench = models.TextField(null=True, blank=True)  
    
    def __str__(self):
        return f"choice: choiceText: {self.choiceTextEnglish} recode: {self.recode}" 

########################################################################################################################################################
    
class UserTable(models.Model):
    
    # Fields/Attributes
    externalDataReference = models.CharField(max_length=15)
    province = models.CharField(max_length=2)   # BC,AB,SK,MB,ON,QC,NB,NS,NL,PI,YK,NV,NW
    size = models.CharField(max_length=2)
    hrtype = models.CharField(max_length=2,default="VO")       # PD,VO

    languagePreference = models.CharField(max_length=2,default='EN')   # EN, FR, BI
    designation = models.CharField(max_length=3) # A = Public (pub), B = Private (prv), C = Charitable (chr)
    locationPolygon = models.CharField(max_length=16)
    urbanRural = models.CharField(max_length=2) # UR/RL
    

    dateFounded = models.DateField(null=True, blank=True)
    age = models.TextField()

    domain = models.TextField()
    subDomain = models.TextField()
    subSample = models.TextField()
    jobTitle = models.TextField()
    region = models.TextField()
    expenditure = models.TextField(default="XS")


    def __str__(self):
         return f"User: \n id: {self.id}\n ref#: {self.externalDataReference}\n prv: {self.province}\n sz: {self.size}\n lng: {self.languagePreference}"


########################################################################################################################################################

class UserResponseTable(models.Model):
    
    # Foreign Keys
    userID = models.ForeignKey(UserTable, on_delete=models.DO_NOTHING,null=True,blank=True)
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE,null=True,blank=True)
    
    # this foriegn key might be redundant since we can access the choice through the question
    choiceID = models.ForeignKey(ChoiceTable, on_delete=models.CASCADE,null=True,blank=True)
    
    # Fields/Attributes
    answerTextOriginal = models.TextField(max_length=4096,null=True)
    answerTextEnglish = models.TextField(max_length=4096,null=True)
    answerTextFrench = models.TextField(max_length=4096,null=True)
    
    answerValue = models.TextField(null=True)
    
    def __str__(self):
        recode = '-1'
        if self.choiceID != None:
            recode = self.choiceID.recode
            
        return f"UserResponse: \nuserID: {self.userID.id} \nquestionID: {self.questionID.id} \nrecode: {recode} \nanswerText: {self.answerTextOriginal} \nanswerValue: {self.answerValue}" 

    # this function returns a dictionary which will be entered into the data file sent to the front end
    # the key:value pair is columnHeader:entry        
    def GetDataFileEntry(self):
    
        userProv = self.userID.province
        userSize = self.userID.size
        userDomain = self.userID.domain
        userLang = self.userID.languagePreference
        # responseTextEnglish = self.answerTextEnglish
        # responseTextFrench = self.answerTextFrench
        responseTextOriginal = self.answerTextOriginal
        responseValue = self.answerValue
        
        choiceRecode = '-1'
        choiceText = ''
        if self.choiceID != None:
            choiceRecode = self.choiceID.recode
            choiceText = self.choiceID.choiceTextEnglish # TODO: handle french
        
        df = pd.DataFrame({ 'userProv' : userProv,
                            'userSize' : userSize,
                            'userDomain' : userDomain,
                            'userLang' : userLang,
                            'choiceRecode' : choiceRecode,
                            'choiceText' : choiceText,
                            'responseTextOriginal' : responseTextOriginal,
                            'responseValue' : responseValue                       
                        }, index=[0])

        return df
    
    def GetDataFileString(self):
    
        userProv = self.userID.province
        userSize = self.userID.size
        userDomain = self.userID.domain
        userLang = self.userID.languagePreference
        responseTextOriginal = self.answerTextOriginal
        responseValue = self.answerValue
        
        choiceRecode = '-1'
        choiceText = ''
        if self.choiceID != None:
            choiceRecode = self.choiceID.recode
            choiceText = self.choiceID.choiceTextEnglish # TODO: handle french
        
        dataFileString =    str(userProv) + ',' + \
                            str(userSize) + ',' + \
                            str(userDomain) + ',' + \
                            str(userLang) + ',' + \
                            str(choiceRecode) + ',' + \
                            str(choiceText) + ',' + \
                            str(responseTextOriginal) + ',' + \
                            str(responseValue)                 
                
        return dataFileString   
    
    # This gives the model an explicit ordering
    class Meta:
        ordering = ('questionID',)