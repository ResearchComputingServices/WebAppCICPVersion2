import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# This function extracts the required data from the english version of the survey file
# the extracted data is stored in Question Objects which are in turn stored in a list
##################################################################################################################################
def ExtractQuestionDataFromJSON(surveyJSON,aSurvey):
     
    # loop over the questions data in the JSON file
    for qDictID in surveyJSON['result']['questions']:          
        
        qDict = surveyJSON['result']['questions'][qDictID]
        
        question = QuestionTable()
        question.surveyID = aSurvey
        question.questionType = qDict['questionType']['type']       
        question.questionName = qDict['questionName']
        question.questionTextEnglish = qDict['questionText']
        question.parentQuestionID = None
        question.save()        
        
        if question.questionType == OPEN_TEXT_QUESTION:
            choice = ChoiceTable()    
            choice.questionID = question
            choice.recode = -1
            choice.choiceTextEnglish = None
            choice.save() 
            
        elif question.questionType == MATRIX_QUESTION:
            if 'subQuestions' in qDict:
                questionCounter = 0
                for subQDictID in qDict['subQuestions']:
                    # Get direct access to the sub question dictionary
                    subQDict = qDict['subQuestions'][subQDictID]
                    
                    # Use data from the sub question dictionary and the question dictionary
                    # to create an entry in the QuestionTable for the sub question
                    subQuestion = QuestionTable()
                    subQuestion.surveyID = aSurvey
                    subQuestion.questionType = qDict['questionType']['type']       
                    subQuestion.questionName = qDict['questionName']+'_'+subQDict['recode']
                    subQuestion.questionTextEnglish = subQDict['choiceText']
                    subQuestion.parentQuestionID = question
                    
                    subQuestion.save()
                    
                    if 'choices' in qDict:
                        for cDictID in qDict['choices']:
                            
                            cDict = qDict['choices'][cDictID]
                            
                            choice = ChoiceTable()
                            
                            choice.questionID = subQuestion
                            choice.recode = cDict['recode']
                            choice.choiceTextEnglish = cDict['choiceText']
                            choice.save() 
                    
                    questionCounter = questionCounter + 1 
        else:
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
    aSurvey.releaseDate = '2023-01-01'
    aSurvey.save()
    ExtractSurveyMain(aSurvey)