from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from WebAppCICPVersion2 import settings

from dataclasses import dataclass, field
from typing import List, Dict
import random
import re 
import os
import textwrap

##################################################################################################################################
# 
##################################################################################################################################

# Question Types
OPEN_TEXT_QUESTION =        'TE'
MULTIPLE_CHOICE_QUESTION =  'MC'
SLIDER_QUESTION =           'Slider'
MATRIX_QUESTION =           'Matrix'
RANK_ORDER_QUESTION =       'RO'
TEXT_GRAPHIC_QUESTION =     'DB'

# Question Themes to skip
SKIP_THEMES = ['Consent','CONSENT','skip','SKIP']

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
# 
##################################################################################################################################

FIGURE_WIDTH_PX = 800
FIGURE_HEIGHT_PX = 600

PIE_CHART_HOLE_RADIUS = 0.5

MAX_TITLE_LENGTH = 75


FONT_LOCATION = os.path.join(settings.BASE_DIR,'fonts','Helvetica_Now_Text__Regular.ttf')

FIGURE_FOLDER_PATH = os.path.join(settings.BASE_DIR, 'tmpImages')

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
# This function ensures that the string passed as an agrument is less than MAX_LEGNTH. It does this by adding a line break 
# to the string when it exceeds the length limit.
##################################################################################################################################

def WrapText(text, titleLength = MAX_TITLE_LENGTH):
    
    text = CleanText(text)
    
    tw = textwrap.TextWrapper(width=titleLength)
    word_list = tw.wrap(text=text)
            
    newTitle = '<br>'.join(word_list)
    
    return newTitle    

##################################################################################################################################
# This function returns the numerical values of the max and min of the graphs range
##################################################################################################################################

def GetRange(allPositive, 
             allNegative,
             defaultMin = 0,
             defaultMax = 10):
    
    xMin = defaultMin
    xMax = defaultMax
    
    if allNegative:
        xMin = -1*defaultMax
        xMax = 0
    elif not allPositive and not allPositive:
        xMin = -1*defaultMax
        xMax = defaultMax
        
    return xMin, xMax 

##################################################################################################################################
# This functions is a helper function for the CreateVerticalBarChart function. It takes the title string from the question 
# DataClass and extracts from it the values and labels for the range of the figure.
##################################################################################################################################

def CreateLabels(titleText):
    tickValues = []
    tickLabels = []

    # get the text in brackets
    bracketText = CleanText(titleText[titleText.find("(")+1:titleText.find(")")])

    # split it by comma
    bracketTextSplit = bracketText.split(',')    
    
    if len(bracketTextSplit) != 0:
        
        # split each pair by colon
        for pair in bracketTextSplit:
            pairSplit = pair.split(':')
            if len(pairSplit) == 2:
                tickValues.append(float(pairSplit[0]))      
                tickLabels.append(pairSplit[1])   
        
    return tickValues, tickLabels  
 
 
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