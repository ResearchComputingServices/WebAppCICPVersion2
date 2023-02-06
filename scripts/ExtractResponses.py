import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# 
##################################################################################################################################
def RemoveMetaDataFromResponse(response):
    userResponseDict = response
    
    for key in RESPONSE_KEYS_TO_REMOVE_LIST:
        if key in userResponseDict:
            userResponseDict.pop(key)
    
    return userResponseDict

##################################################################################################################################
# 
##################################################################################################################################
def GetResponsesToQuestion(userResponses, currentQuestionName):
    
    listOfResponsesToQuestion = []

    for response in userResponses:
        tokens = response.split('_')
 
        if currentQuestionName in tokens:
            listOfResponsesToQuestion.append(response)
       
    return listOfResponsesToQuestion

##################################################################################################################################
# 
##################################################################################################################################
def GetUserResponse(user = None, question = None, choice = None):
    userResponse = None
    
    userResponseQuerySet = UserResponseTable.objects.filter(userID = user,
                                                            questionID = question,
                                                            choiceID = choice)
    
    if len(userResponseQuerySet) == 1:
        userResponse = userResponseQuerySet.first()
    elif len(userResponseQuerySet) == 0:
        userResponse = UserResponseTable()
        
        userResponse.userID = user
        userResponse.questionID = question  
        userResponse.choiceID = choice
        
    else:
        print('[WARNING]: multiple user responses to question...')    
    
    return userResponse

##################################################################################################################################
# 
##################################################################################################################################
def GetRecodeFromResponseKey(responseKey,responseValue):
    tokens = responseKey.split('_')   
    recodeValue = -1

    if len(tokens) == 1:
        recodeValue = responseValue

    if len(tokens) == 2 and 'TEXT' not in tokens:
        recodeValue = tokens[1]

    if len(tokens) == 3:
        recodeValue = tokens[1]
                        
    return recodeValue

##################################################################################################################################
# 
##################################################################################################################################
def GetChoiceEntity(question, responseKey, responseValue):
    
    choice = None
    
    recodeValue = GetRecodeFromResponseKey(responseKey,responseValue)
    
    choiceQuerySet = ChoiceTable.objects.filter(recode=recodeValue,
                                                questionID=question)
    if len(choiceQuerySet) == 1:
        choice = choiceQuerySet.first()
    
    return choice

##################################################################################################################################
# 
##################################################################################################################################
def ExtractTextQuestionResponse(question, userResponsesList):

    # the userResponses object is a dictionary of responses to questions    
    for userResponses in userResponsesList:
   
        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, question.questionName)
               
        for response in userResponse2CurQ:
            
            responseValue = userResponses[response]
            
            if responseValue == '':
                continue
            
            userResponse = GetUserResponse(user, question)
            userResponse.answerText = responseValue
            userResponse.save()
        
##################################################################################################################################
# 
##################################################################################################################################
def ExtractMultipleChoiceQuestionResponse(question, userResponsesList):

    # the userResponses object is a dictionary of responses to questions    
    for userResponses in userResponsesList:
   
        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, question.questionName)
               
        for responseKey in userResponse2CurQ:
            responseValue = userResponses[responseKey]
            
            if responseValue == '':
                continue
                        
            choice = GetChoiceEntity(question, responseKey, responseValue)
                                 
            userResponse = GetUserResponse(user, question, choice)
                           
            if "TEXT" in responseKey:
                userResponse.answerText = responseValue
            else:
                userResponse.answerValue = responseValue

            userResponse.save()
        
##################################################################################################################################
# 
##################################################################################################################################
def ExtractSliderQuestionResponse(question, userResponsesList):
        
    # the userResponses object is a dictionary of responses to questions    
    for userResponses in userResponsesList:
   
        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, question.questionName)
                
        for responseKey in userResponse2CurQ:
        
            responseValue = userResponses[responseKey]
            if responseValue == '':
                continue
                       
            choice = GetChoiceEntity(question, responseKey, responseValue)
            
            userResponse = GetUserResponse(user, question, choice)
                         
            if "TEXT" in responseKey:
                userResponse.answerText = responseValue
            else:
                userResponse.answerValue = responseValue
                
            userResponse.save()
        
##################################################################################################################################
# 
##################################################################################################################################
def ExtractMatrixQuestionResponse(question, userResponsesList):
    
    # Skip the base question
    if question.parentQuestionID == None:
        return   
    
    # the userResponses object is a dictionary of responses to questions                    
    for userResponses in userResponsesList:

        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, 
                                                   question.questionName.split('_')[0])
              
        for responseKey in userResponse2CurQ:
            
            if responseKey != question.questionName:
                continue
                    
            responseValue = userResponses[responseKey]
        
            if responseValue == '':
                continue
                   
            choice = GetChoiceEntity(question, responseKey, responseValue)
            
            userResponse = GetUserResponse(user, question, choice)
                        
            if "TEXT" in responseKey:
                userResponse.answerText = responseValue
            else:
                userResponse.answerValue = responseValue
                
            userResponse.save()

##################################################################################################################################
# 
##################################################################################################################################
def ExtractTextGraphicQuestionResponse(question, userResponsesList):

    # the userResponses object is a dictionary of responses to questions    
    for userResponses in userResponsesList:
   
        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, question.questionName)
               
        for response in userResponse2CurQ:
            
            responseValue = userResponses[response]
            if responseValue == '':
                continue
            
            userResponse = GetUserResponse(user, question)
            userResponse.answerText = responseValue
            userResponse.save()
                   
##################################################################################################################################
# 
##################################################################################################################################
def ExtractRankOrderQuestionResponse(question, userResponsesList):
    
    # the userResponses object is a dictionary of responses to questions    
    for userResponses in userResponsesList:
        
        externalRefNum = userResponses[EXTERNAL_REF_KEY]
        user = GetUser(externalRefNum) 
        
        userResponse2CurQ = GetResponsesToQuestion(userResponses, question.questionName)
                
        for responseKey in userResponse2CurQ:
        
            responseValue = userResponses[responseKey]
            if responseValue == '':
                continue
                       
            choice = GetChoiceEntity(question, responseKey, responseValue)
            
            userResponse = GetUserResponse(user, question, choice)
                        
            if "TEXT" in responseKey:
                userResponse.answerText = responseValue
            else:
                userResponse.answerValue = responseValue
            userResponse.save()       
    
##################################################################################################################################
# 
##################################################################################################################################
def ExtractResponseDataFromJSON(userResponsesList, aSurvey):

    currentSurveyQuestions = QuestionTable.objects.filter(surveyID=aSurvey)
    
    for question in currentSurveyQuestions:
                
        if question.questionType == OPEN_TEXT_QUESTION:
            ExtractTextQuestionResponse(question, userResponsesList)  
        
        elif question.questionType == MULTIPLE_CHOICE_QUESTION:
            ExtractMultipleChoiceQuestionResponse(question, userResponsesList)  
        
        elif question.questionType == SLIDER_QUESTION:
            ExtractSliderQuestionResponse(question, userResponsesList)  
        
        elif question.questionType == MATRIX_QUESTION:
            ExtractMatrixQuestionResponse(question, userResponsesList)  
        
        elif question.questionType == RANK_ORDER_QUESTION:
            ExtractRankOrderQuestionResponse(question, userResponsesList)  
            
        elif question.questionType == TEXT_GRAPHIC_QUESTION:
            ExtractTextGraphicQuestionResponse(question, userResponsesList)     
                
        else:
            print('[Warning] Unknown question type:\n',question)
                
##################################################################################################################################
# 
##################################################################################################################################  
def GetResponseListFromJSONData(responseDataJSON):
    userResponsesList = []

    for response in responseDataJSON['responses']:
        userResponseDict = RemoveMetaDataFromResponse(response)
        
        userResponsesList.append(userResponseDict)

    return userResponsesList

##################################################################################################################################
# Main function 
##################################################################################################################################  
def ExtractResponsesMain(aSurvey=None):    
    
    responseJSONFilePath =  ''
    if aSurvey != None:
        responseJSONFilePath = os.path.join(settings.BASE_DIR, 
                                            settings.DATA_DIR_PATH, 
                                            aSurvey.qualtricsSurveyID, 
                                            settings.RESPONSE_DATA_JSON_FILENAME)
    else:
        print('[ERROR]: ExtractResponsesMain: no surveyID given')
        return
    
    responseDataJSON= ''
    with open(responseJSONFilePath) as f:
        responseDataJSON = json.load(f)

    # Get rid of all the metadata in the response dictionary and return it
    # as a list of responses
    userResponsesList = GetResponseListFromJSONData(responseDataJSON)

    ExtractResponseDataFromJSON(userResponsesList, aSurvey) 
    
    # ToDo: this should only return true if the retrieval process worked
    return True  
         
##################################################################################################################################
# This function always the script to be tested using the Django runscript formalism
##################################################################################################################################

def run(*args):

    surveyQuerySet = SurveyTable.objects.filter(qualtricsSurveyID = settings.TEST_SURVEY_ID)

    if len(surveyQuerySet) == 1:
        ExtractResponsesMain(surveyQuerySet.first()) 
    else:
        print('[Warning] no unique survey found with qualtricsSurveyID:', settings.TEST_SURVEY_ID)