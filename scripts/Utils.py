from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from dataclasses import dataclass, field
from typing import List, Dict
import random
import re 

##################################################################################################################################
# 
##################################################################################################################################

# Question Types
OPEN_TEXT_QUESTION =        'TE'
MULTIPLE_CHOICE_QUESTION =  'MC'
SLIDER_QUESTION =           'Slider'
MATRIX_QUESTION =           'Matrix'
RANK_ORDER_QUESTION =       'RO'


EXTERNAL_REF_KEY = 'ExternalDataReference'

# These are the key:value pairs which are removed from the response JSON file to make it easier to 
# extract the responses
RESPONSE_KEYS_TO_REMOVE_LIST = ['ResponseID',
                                'ResponseSet',
                                'IPAddress',
                                'StartDate',
                                'EndDate',
                                'RecipientLastName',
                                'RecipientFirstName',
                                'RecipientEmail',
                                'Finished',
                                'Status',
                                'LocationLatitude',
                                'LocationLongitude',
                                'LocationAccuracy',
                                'Consent']

##################################################################################################################################
# This dataClass contains all the values which the user wants to filter on
# it should be created by the viewer and passed to the controller
##################################################################################################################################

@dataclass
class FrontEndQuery:
    
    # Filter on Survey
    date: str = None
    
    # Filter on Question
    questionThemes: List = field(default_factory=lambda: [])  
    
    # Filter on User
    locations: List = field(default_factory=lambda: []) 
    organizationSizes: List = field(default_factory=lambda: []) 
    languagePreference: List = field(default_factory=lambda: []) 
    fieldOfWork: List = field(default_factory=lambda: []) 
 
##################################################################################################################################
# This function removes any text in brackets and replaces special characeter codes with the actual character
##################################################################################################################################

def CleanText(text):
    cleanedText = text
    cleanedText= cleanedText.replace("\n","")
    cleanedText = re.sub("[\[].*?[\]]", "", cleanedText)
    cleanedText = re.sub("[\(].*?[\)]", "", cleanedText)
    cleanedText = re.sub("[\<].*?[\>]", "", cleanedText)
    cleanedText = cleanedText.replace('&rsquo;','\'')
    cleanedText = cleanedText.replace('&lsquo;','\'')
    cleanedText = cleanedText.replace('&#39;','\'')
        
    return cleanedText
 
##################################################################################################################################
# 
##################################################################################################################################
def GetQuestion(aSurvey,questionName):
    
    questionQuerySet = QuestionTable.objects.filter(surveyID=aSurvey, questionName=questionName)
        
    if len(questionQuerySet) == 1:
        return questionQuerySet.first()
    else:
        print('[ERROR]: GetQuestion: questionName is not unique: ', aSurvey, questionName)

##################################################################################################################################
# 
##################################################################################################################################
def GetSurveyQuestionsFromDB(qualtricsSurveyID):
    survey = SurveyTable.objects.filter(qualtricsSurveyID=qualtricsSurveyID).first()
    surveyQuestions = QuestionTable.objects.filter(surveyID=survey.id) 

    return surveyQuestions

##################################################################################################################################
# 
##################################################################################################################################
def GetSurvey(qualtricSurveyID):
    surveyQuerySet = SurveyTable.objects.filter(qualtricsSurveyID=qualtricSurveyID)
    
    survey = None
    if len(surveyQuerySet) == 1:
        survey = surveyQuerySet.first()
    else:
        print('[ERROR]: GetSurvey: qualtricsSurveyID is not unique: ', qualtricSurveyID, len(surveyQuerySet))
    
    return survey

##################################################################################################################################
# 
##################################################################################################################################
def GetUser(externalRefNum):
    
    userQuerySet = UserTable.objects.filter(externalDataReference=externalRefNum)
    user = None
    if len(userQuerySet) == 1:
        user = userQuerySet.first()      
    else:    
        ##########################################################
        # Remove this could after development
        # replace it with code to handle a user doesnt exist
        user = UserTable()
        user.externalDataReference = externalRefNum
        user.province = 'AB'
        user.size = 'small'
        user.domain = 'other'
        user.languagePreference = 'EN'
        user.save()
        ##########################################################

    return user