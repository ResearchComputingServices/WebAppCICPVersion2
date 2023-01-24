from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# 
##################################################################################################################################

def run(*args):
        
    surveyQuestions = GetSurveyQuestionsFromDB(settings.TEST_SURVEY_ID)
    
    for question in surveyQuestions:
        print(question)
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        questionChoices = ChoiceTable.objects.filter(questionID=question)
        userResponses = UserResponseTable.objects.filter(questionID=question)
        for choice in questionChoices:
            print(choice)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
        for response in userResponses:
            print(response)
            input()