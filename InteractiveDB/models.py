from django.db import models

# on_delete defines what to do with the current table if the foreign key is deleted

class SurveyTable(models.Model):    
    # Fields/Attributes
    qualtricsSurveyID = models.CharField(max_length=30)
    releaseDate = models.DateField()
    fetchedDate = models.DateField(null=True,blank=True)
       
    def __str__(self):
        return f"id: {self.id} surveyID: {self.qualtricsSurveyID} date: {self.releaseDate}"
    
            
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
   
    questionTheme = models.TextField() 
   
    jsonKey = models.TextField() # used for matching with french survey file
   
    def __str__(self):
        return f"Question: \n id: {self.id} \n type: {self.questionType} \n theme: {self.questionTheme} \n text: {self.questionTextEnglish} "   
    
class ChoiceTable(models.Model):
    
    # Foreign Keys
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    
    # Fields/Attributes
    recode = models.IntegerField()
    choiceTextEnglish = models.TextField(null=True, blank=True)
    choiceTextFrench = models.TextField(null=True, blank=True)  
    
    def __str__(self):
        return f"choice: choiceText: {self.choiceTextEnglish} recode: {self.recode}" 
    
class UserTable(models.Model):
    
    # Fields/Attributes
    externalDataReference = models.CharField(max_length=15)
    province = models.CharField(max_length=2)   # BC,AB,SK,MB,ON,QC,NB,NS,NL,PI,YK,NV,NW
    size = models.CharField(max_length=6)       # small, medium, large
    domain = models.CharField(max_length=30)
    languagePreference = models.CharField(max_length=2)   #EN, FR

    def __str__(self):
         return f"User: \n id: {self.id}\n ref#: {self.externalDataReference}\n prv: {self.province}"

class UserResponseTable(models.Model):
    
    # Foreign Keys
    userID = models.ForeignKey(UserTable, on_delete=models.DO_NOTHING)
    questionID = models.ForeignKey(QuestionTable, on_delete=models.CASCADE)
    
    # this foriegn key might be redundant since we can access the choice through the question
    choiceID = models.ForeignKey(ChoiceTable, on_delete=models.CASCADE,null=True,blank=True)
    
    # Fields/Attributes
    answerText = models.TextField(null=True)
    answerValue = models.TextField(null=True)
    
    def __str__(self):
        recode = '-1'
        if self.choiceID != None:
            recode = self.choiceID.recode
            
        return f"UserResponse: \nuserID: {self.userID.id} \nquestionID: {self.questionID.id} \nrecode: {recode} \nanswerText: {self.answerText} \nanswerValue: {self.answerValue}" 

    # this function returns a dictionary which will be entered into the data file sent to the front end
    # the key:value pair is columnHeader:entry        
    def GetDataFileEntry(self):
        
        questionKey = self.questionID.jsonKey
        questionText = self.questionID.questionTextEnglish # TODO: handle fench as well
        questionTheme = self.questionID.questionTheme
        
        userProv = self.userID.province
        userSize = self.userID.size
        userDomain = self.userID.domain
        userLang = self.userID.languagePreference
        
        choiceRecode = '-1'
        choiceText = ''
        if self.choiceID != None:
            choiceRecode = self.choiceID.recode
            choiceText = self.choiceID.choiceTextEnglish # TODO: handle french
        
        responseText = self.answerText
        responseValue = self.answerValue
            
        entryDict = {   'QuestionKey' : questionKey,
                        'QuestionText' : questionText,
                        'QuestionTheme' : questionTheme, 
                        'userProv' : userProv,
                        'userSize' : userSize,
                        'userDomain' : userDomain,
                        'userLang' : userLang,
                        'choiceRecode' : choiceRecode,
                        'choiceText' : choiceText,
                        'responseText' : responseText,
                        'responseValue' : responseValue                       
                    }      
        
        return entryDict
    
    # This gives the model an explicit ordering
    class Meta:
        ordering = ('questionID',)