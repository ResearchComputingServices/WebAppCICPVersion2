import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# Extracts the survey data from the JSON file and returns it in a SurveyTable object
# This function is no longer needed...I think...
##################################################################################################################################
# def ExtractSurveyDataFromJSON(surveyJSON):
#     survey = SurveyTable()

#     # Get the survey ID 
#     survey.qualtricsSurveyID = surveyJSON['result']['id']
    
#     # Get the creation date
#     # Format example 2022-08-25T20:24:37Z
#     survey.releaseDate = surveyJSON['result']['creationDate'][:10]  
    
#     survey.save()
        
#     return survey

##################################################################################################################################
# This function extracts the required data from the english version of the survey file
# the extracted data is stored in Question Objects which are in turn stored in a list
##################################################################################################################################
def ExtractQuestionDataFromJSON(surveyJSON,survey):
     
    # loop over the questions data in the JSON file
    for qDictID in surveyJSON['result']['questions']:          
        
        qDict = surveyJSON['result']['questions'][qDictID]
        
        question = QuestionTable()
        question.surveyID = survey
        question.questionType = qDict['questionType']['type']       
        question.questionName = qDict['questionName']
        question.questionTextEnglish = qDict['questionText']
        question.save()
                
        if 'choices' in qDict:
            for cDictID in qDict['choices']:
                
                cDict = qDict['choices'][cDictID]
                
                choice = ChoiceTable()
                
                choice.questionID = question
                choice.recode = cDict['recode']
                choice.choiceTextEnglish = cDict['choiceText']
                choice.save()
        
##################################################################################################################################
# Main function 
##################################################################################################################################  

def ExtractSurveyMain(aSurvey=None):

    successFlag = False

    if aSurvey == None:
        print('[ERROR]: could not retrieve survey from DB: None')
        successFlag = False
    else:
        # open the english language JSON file
        englishJSONFilePath =  ''
        if aSurvey != None:
            englishJSONFilePath = os.path.join( settings.BASE_DIR, 
                                                settings.DATA_DIR_PATH, 
                                                aSurvey.qualtricsSurveyID, 
                                                settings.QUESTION_ENGLISH_JSON_FILENAME)            
            englishSurveyJSON= ''
            with open(englishJSONFilePath) as f:
                englishSurveyJSON = json.load(f)

            ExtractQuestionDataFromJSON(englishSurveyJSON, aSurvey)
            successFlag = True
        else:
            print('[ERROR]: ExtractSurveyMain: no surveyID given')
            successFlag = False
    
    return successFlag
        
################################################################################################################################## 
# This function always the script to be tested using the Django runscript formalism
################################################################################################################################## 

def run(*args):
    aSurvey = SurveyTable()
    aSurvey.qualtricsSurveyID = settings.TEST_SURVEY_ID
    ExtractSurveyMain(aSurvey)