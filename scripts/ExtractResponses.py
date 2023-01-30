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
def InterpretResponseKey(responseKey):
    tokens = responseKey.split('_')
    
    questionName = ''
    recodeValue = -1
    textFlag = False
    
    # the first token in the reponse key is always the "questionName"
    questionName = tokens[0]
    
    # the "TEXT" identifier can be in either the 2nd or 3rd location
    if 'TEXT' in tokens:
        textFlag = True
        
    # the "recode" identifier can be in either the 2nd or 3rd location
    if len(tokens) == 2:
        if tokens[1].isnumeric():
            recodeValue = tokens[1]
    
    # for some question types the responsekey is only 2 items long
    if len(tokens) == 3:
        if tokens[2].isnumeric():
            recodeValue = tokens[2]
                
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
    print(question)
    print(user)
    print(responseValue)
    print(recodeValue)
    print(textFlag)
    
    choice = ChoiceTable.objects.filter(questionID=question.id,
                                        recode=recodeValue).first()
                
    userResponseQuery = UserResponseTable.objects.filter(userID=user.id,
                                                            questionID=question.id,
                                                            choiceID=choice.id)
    userResponse = None
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
def ExtractResponseDataFromJSON(responseDataJSON, aSurvey):

    
    for response in responseDataJSON['responses']:
        
        # the externalReferenceNumber is used to connect the response to a user in the UserTable
        externalRefNum = response['ExternalDataReference']   
        user = GetUser(externalRefNum)      
        
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
            question = GetQuestion(aSurvey,questionName)
            
            userResponse = None
            if recodeValue == -1:
                userResponse = HandleFreeTextResponse(question, user, responseValue)
            else:
                userResponse = HandleChoiceResponse(question, user, responseValue, recodeValue, textFlag)

            userResponse.save()    

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

    ExtractResponseDataFromJSON(responseDataJSON, aSurvey) 
    
    # ToDo: this should only return true if the retrieval process worked
    return True  
         
##################################################################################################################################
# This function always the script to be tested using the Django runscript formalism
##################################################################################################################################

def run(*args):
   ExtractResponsesMain(settings.TEST_SURVEY_ID) 