from django.db.models import Q

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

##################################################################################################################################
# 
##################################################################################################################################
def GetUserQuerySet(aQuery):
    userQuerySet = UserTable.objects.all()
       
    if len(aQuery.locations) != 0:
        userQuerySet = userQuerySet.filter(province=aQuery.locations)

    
    if len(aQuery.organizationSizes) != 0:
        userQuerySet = userQuerySet.filter(size=aQuery.organizationSizes)
  
    
    if len(aQuery.languagePreference) != 0:
        userQuerySet = userQuerySet.filter(languagePreference=aQuery.languagePreference)
  
        
    if len(aQuery.fieldOfWork) != 0:
        userQuerySet = userQuerySet.filter(domain=aQuery.fieldOfWork)
  
    return userQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetQuestionQuerySet(aQuery):
    questionQuerySet = QuestionTable.objects.all()
    surveyQuerySet = SurveyTable.objects.all()
       
    if aQuery.date != None:
        surveyQuerySet = surveyQuerySet.filter(releaseDate=aQuery.date)
    
    if len(aQuery.questionThemes) != 0:
        questionQuerySet = questionQuerySet.filter(questionTheme=aQuery.questionThemes)
        
    qObject = Q()
    for e in surveyQuerySet:
        qObject |= Q(surveyID=e.id)
      
    questionQuerySet = questionQuerySet.filter(qObject)
   
    return questionQuerySet

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery):
    
    questionQuerySet = GetQuestionQuerySet(aQuery)
    userQuerySet = GetUserQuerySet(aQuery)
        
    qObject = Q()
    for q in questionQuerySet:
        for u in userQuerySet:
            qObject |= Q(questionID=q.id, userID = u.id)
        
    userResponseQuerySet = UserResponseTable.objects.filter(qObject)
    
    return userResponseQuerySet
    
##################################################################################################################################
# This function is used to test the controller functions
##################################################################################################################################
def run(*arg):
    aQuery = FrontEndQuery()   
    aQuery.date = '2023-01-03'
    aQuery.locations = 'AB'

    userResponseQuerySet = HandleFrontEndQuery(aQuery)
    
    print('# of responses found:', len(userResponseQuerySet))
    
    for userResponse in userResponseQuerySet:
        print(userResponse)
        input()