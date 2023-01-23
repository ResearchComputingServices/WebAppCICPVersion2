from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

##################################################################################################################################
# 
##################################################################################################################################

def run(*args):
        
    surveyQuestions = GetSurveyQuestionsFromDB(TEST_SURVEY_ID)
    
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