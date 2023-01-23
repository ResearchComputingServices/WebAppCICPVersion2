import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

##################################################################################################################################
# 
##################################################################################################################################
def RemoveMetaDataFromResponse(response):
    userResponseDict = response
    
    for key in RESPONSE_KEYS_TO_REMOVE_LIST:
        userResponseDict.pop(key)
    
    return userResponseDict

##################################################################################################################################
# 
##################################################################################################################################
def InterpretResponseKey(responseKey):
    tokens = responseKey.split('_')
    
    questionName = ''
    recodeValue = ''
    textFlag = False
    
    if len(tokens) == 1:
        questionName = tokens[0]
        recodeValue = -1    
    elif len(tokens) == 2:
        questionName = tokens[0]
        recodeValue = tokens[1]
    elif len(tokens) == 3:
        questionName = tokens[0]
        recodeValue = tokens[1]
        textFlag = True
    else:
        print("[ERROR] InterpretResponseKey: Unknown responseKey format: ", responseKey)
        
    return questionName, recodeValue, textFlag

##################################################################################################################################
# 
##################################################################################################################################
def HandleFreeTextResponse(question, user, responseValue):
    userResponse = UserResponseTable()
    userResponse.userID = user
    userResponse.questionID = question  
    userResponse.answerText = responseValue

    return userResponse  

##################################################################################################################################
# 
##################################################################################################################################
def  HandleChoiceResponse(question, user, responseValue,recodeValue, textFlag):
    choice = ChoiceTable.objects.filter(questionID=question.questionID,
                                            recode=recodeValue).first()
                
    userResponseQuery = UserResponseTable.objects.filter(userID=user.userID,
                                                            questionID=question.questionID,
                                                            choiceID=choice.choiceID)
    userResponse = ''
    if len(userResponseQuery) == 0:
        userResponse = UserResponseTable()
        userResponse.userID = user
        userResponse.questionID = question
        userResponse.choiceID = choice
        
        # if the text flag is true than the text for the answer is in the responseValue
        if textFlag:
            userResponse.answerText = responseValue
        # if not than the response text is in the choice
        else:
            userResponse.answerValue = responseValue
        
    else:
        userResponse = userResponseQuery.first()
        # if the text flag is true than the text for the answer is in the responseValue
        if textFlag:
            userResponse.answerText = responseValue
        # if not than the response text is in the choice
        else:
            userResponse.answerValue = responseValue 
    
    return userResponse 
    
##################################################################################################################################
# 
##################################################################################################################################
def ExtractResponseDataFromJSON(responseDataJSON):

    surveyID = GetSurveyID(TEST_SURVEY_ID)

    for response in responseDataJSON['responses']:
        
        # the externalReferenceNumber is used to connect the response to a user in the UserTable
        externalRefNum = response['ExternalDataReference']   
        
        # ToDo: Move this to a function called GetUser
        userQuerySet = UserTable.objects.filter(externalDataReference=externalRefNum)
        user = ''
        if len(userQuerySet) == 1:
            user = userQuerySet.first()      
        else:    
            continue
        
        # remove all the "meta" data from the response so that all that is left is the answer data
        userResponseDict = RemoveMetaDataFromResponse(response)          
       
        # loop over the responses
        # responses are handle differently depending on the values recieved from the InterpretResonseKey function
        for responseKey in userResponseDict:
            responseValue = userResponseDict[responseKey]
            
            # Skip blank responses
            if responseValue == '':
                continue
            
            questionName, recodeValue, textFlag = InterpretResponseKey(responseKey)
            question = GetQuestion(surveyID,questionName)
            
            userResponse = ''
            if recodeValue == -1:
                userResponse = HandleFreeTextResponse(question, user, responseValue)
            else:
                userResponse = HandleChoiceResponse(question, user, responseValue, recodeValue, textFlag)

            userResponse.save()    
         
         
##################################################################################################################################
# 
##################################################################################################################################

def run(*args):
     # open the english language JSON file
    responseJSONFilePath = os.path.join(baseDir, dataDirPath, TEST_SURVEY_ID,responseDataJSONFileName)
   
    responseDataJSON= ''
    with open(responseJSONFilePath) as f:
        responseDataJSON = json.load(f)

    ExtractResponseDataFromJSON(responseDataJSON)