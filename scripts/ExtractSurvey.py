import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# This function extracts the required data from the english version of the survey file
# the extracted data is stored in Question Objects which are in turn stored in a list
##################################################################################################################################
def ExtractQuestionDataFromEnglishJSON(surveyJSON,aSurvey):
     
    # loop over the questions data in the JSON file
    for qDictID in surveyJSON['result']['questions']:          
        
        qDict = surveyJSON['result']['questions'][qDictID]
        
        question = QuestionTable()
        question.surveyID = aSurvey
        question.questionType = qDict['questionType']['type']       
        question.questionName = qDict['questionName']
        question.questionTextEnglish = CleanText(qDict['questionText'])
        question.parentQuestionID = None
        question.jsonKey = qDictID
        
        # populate the questionTheme field 
        question.questionTheme = ''
        questionLabelField = qDict['questionLabel']
        if questionLabelField != None:
            questionLabelFieldSplit = questionLabelField.split('_')
            if len(questionLabelFieldSplit) >= 1:
                question.questionTheme = questionLabelFieldSplit[0]
           
        question.save()        
        
        if question.questionType == OPEN_TEXT_QUESTION:
            choice = ChoiceTable()    
            choice.questionID = question
            choice.recode = -1
            choice.choiceTextEnglish = None
            choice.save() 
            
        elif question.questionType == MATRIX_QUESTION:
            if 'subQuestions' in qDict:

                for subQDictID in qDict['subQuestions']:
                    # Get direct access to the sub question dictionary
                    subQDict = qDict['subQuestions'][subQDictID]
                    
                    # Use data from the sub question dictionary and the question dictionary
                    # to create an entry in the QuestionTable for the sub question
                    subQuestion = QuestionTable()
                    
                    subQuestion.surveyID = aSurvey
                    subQuestion.questionType = qDict['questionType']['type']       
                    subQuestion.questionName = qDict['questionName']+'_'+subQDict['recode']
                    subQuestion.questionTextEnglish = CleanText(subQDict['choiceText'])
                    subQuestion.parentQuestionID = question
                    subQuestion.questionTheme = question.questionTheme
                    
                    subQuestion.save()

                    if 'choices' in qDict:
                        for cDictID in qDict['choices']:
                            
                            cDict = qDict['choices'][cDictID]
                            
                            choice = ChoiceTable()
                            
                            choice.questionID = subQuestion
                            choice.recode = cDict['recode']
                            choice.choiceTextEnglish = CleanText(cDict['choiceText'])
                            choice.save() 
                    
        else:
            if 'choices' in qDict:
                for cDictID in qDict['choices']:
                    
                    cDict = qDict['choices'][cDictID]
                    
                    choice = ChoiceTable()
                    
                    choice.questionID = question
                    choice.recode = cDict['recode']
                    choice.choiceTextEnglish = CleanText(cDict['choiceText'])
                    choice.save()   

##################################################################################################################################
# 
##################################################################################################################################  
def ExtractQuestionDataFromFrenchJSON(surveyJSON, aSurvey):                   
    
    frenchSurveyTextDict = surveyJSON['result']
    
    for key in frenchSurveyTextDict:
            
        keySplit = key.split('_')
        
        if 'QuestionText' in key:
           
            questionJSONKey = keySplit[0]
            questionTextFrench = CleanText(frenchSurveyTextDict[key])
            
            question = QuestionTable.objects.filter(jsonKey = questionJSONKey, surveyID = aSurvey.id).first()
            
            question.questionTextFrench = questionTextFrench
            
            question.save()
            
        elif 'Choice' in key:
            
            questionJSONKey = keySplit[0]
            recode = int(keySplit[1][6:])
            
            choiceTextFrench = CleanText(frenchSurveyTextDict[key])
            
            question = QuestionTable.objects.filter(jsonKey = questionJSONKey, surveyID = aSurvey.id).first()
            
            if question.questionType != MATRIX_QUESTION:
                choice = ChoiceTable.objects.filter(questionID = question.id, recode = recode).first()           
                if choice != None:           
                    choice.choiceTextFrench = choiceTextFrench
                    choice.save()
            else:
                recode = keySplit[1][6:]
                
                subQuestionName =  question.questionName+'_'+recode

                subQuestion = QuestionTable.objects.filter(questionName = subQuestionName, surveyID = aSurvey.id).first()
                subQuestion.questionTextFrench = choiceTextFrench  
                
                subQuestion.save()
            
        elif 'Answer' in key:
            
            questionJSONKey = keySplit[0]
            recode = keySplit[1][6:]
                      
            question = QuestionTable.objects.filter(jsonKey = questionJSONKey, surveyID = aSurvey.id).first()
            subQuestionQuerySet = QuestionTable.objects.filter(parentQuestionID = question.id)
                       
            for subQuestion in subQuestionQuerySet:
            
                choice = ChoiceTable.objects.filter(questionID = subQuestion.id, recode = recode).first()           
            
                choiceTextFrench = CleanText(frenchSurveyTextDict[key])
                choice.choiceTextFrench = choiceTextFrench
            
                choice.save()  
                   
##################################################################################################################################
# Return a dictionary containing the contents of JSON file 
##################################################################################################################################  
def OpenSurveyJSONFile(qualtricsSurveyID, languageFlag):
    
    filename = ''
    if languageFlag == 'EN':
        filename = settings.QUESTION_ENGLISH_JSON_FILENAME
    elif languageFlag == 'FR':
        filename = settings.QUESTION_FRENCH_JSON_FILENAME
    else:
        print('[ERROR]: OpenSurveyJSONFile: Unknown LanguageFlag: ', languageFlag)
        return None
    
    JSONFilePath = os.path.join(settings.BASE_DIR, 
                                settings.DATA_DIR_PATH, 
                                qualtricsSurveyID, 
                                filename)            
    surveyJSON = None
    with open(JSONFilePath) as f:
        surveyJSON = json.load(f)
        
    return surveyJSON
    
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
        if aSurvey != None:
            englishSurveyJSON = OpenSurveyJSONFile(aSurvey.qualtricsSurveyID, 'EN')
            ExtractQuestionDataFromEnglishJSON(englishSurveyJSON, aSurvey)
            
            frenchSurveyJSON = OpenSurveyJSONFile(aSurvey.qualtricsSurveyID, 'FR')
            ExtractQuestionDataFromFrenchJSON(frenchSurveyJSON, aSurvey)
            
            successFlag = True
        else:
            print('[ERROR]: ExtractSurveyMain: no surveyID given')
            successFlag = False
    
    return successFlag
        
################################################################################################################################## 
# This function always the script to be tested using the Django runscript formalism
################################################################################################################################## 

def run(*args):
    surveyQuerySet = SurveyTable.objects.all()
        
    for survey in surveyQuerySet:
        print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)

        HandleReleasedSurvey(survey,currentDate)
