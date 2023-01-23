import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable

##################################################################################################################################
# Extracts the survey data from the JSON file and returns it in a SurveyTable object
##################################################################################################################################
def ExtractSurveyDataFromJSON(surveyJSON):
    survey = SurveyTable()

    # Get the survey ID 
    survey.qualtricsSurveyID = surveyJSON['result']['id']
    
    # Get the creation date
    # Format example 2022-08-25T20:24:37Z
    survey.releaseDate = surveyJSON['result']['creationDate'][:10]  
    
    survey.save()
        
    return survey

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

def ExtractSurveyMain():

     # open the english language JSON file
    englishJSONFilePath = os.path.join(baseDir, dataDirPath, TEST_SURVEY_ID, questionEnglishJSONFileName)  
    englishSurveyJSON= ''
    with open(englishJSONFilePath) as f:
        englishSurveyJSON = json.load(f)

    survey = ExtractSurveyDataFromJSON(englishSurveyJSON)
    ExtractQuestionDataFromJSON(englishSurveyJSON, survey)
        
################################################################################################################################## 

def run(*args):
    ExtractSurveyMain()