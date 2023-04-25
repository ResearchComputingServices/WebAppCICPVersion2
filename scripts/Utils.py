from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from WebAppCICPVersion2 import settings

from dataclasses import dataclass, field
from typing import List
import re 
import os
from textwrap import fill
import textwrap
from datetime import datetime

import math

A_LARGE_NUMBER = 99999999999

##################################################################################################################################
# 
##################################################################################################################################

# Minimum number of users allowed in userQuerySize (this is for user anominity/data secured reasons)
MINIMUM_USER_QUERY_SIZE = 10

# Question Types
OPEN_TEXT_QUESTION =        'TE'
MULTIPLE_CHOICE_QUESTION =  'MC'
SLIDER_QUESTION =           'Slider'
MATRIX_QUESTION =           'Matrix'
RANK_ORDER_QUESTION =       'RO'
TEXT_GRAPHIC_QUESTION =     'DB'

# Question Themes to skip
QUESTION_THEME_SKIP_LIST = ['Consent','CONSENT','skip','SKIP']

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

GRAPHIC_FILE_TYPE = 'png'
GRAPHIC_FILE_SUFFIX = '.'+GRAPHIC_FILE_TYPE

##################################################################################################################################
# 
##################################################################################################################################

IMAGE_LIFE_TIME_SECONDS = 259200. # 72 hours

FIGURE_WIDTH_PX = 1200
FIGURE_HEIGHT_PX = 1000

PIE_CHART_HOLE_RADIUS = 0.5

MAX_TITLE_LENGTH = 75

FONT_LOCATION = os.path.join(settings.BASE_DIR,'fonts','Helvetica_Now_Text__Regular.ttf')

TMP_FIGURE_FOLDER_PATH = os.path.join(settings.MEDIA_ROOT, 'tmpImages')

DEFAULT_FIGURE_FOLDER_PATH = os.path.join(settings.MEDIA_ROOT, 'DefaultImages')
#DEFAULT_FIGURE_FOLDER_PATH = os.path.join(settings.BASE_DIR, 'media')

WATERMARK_IMAGE_FILE_PATH = os.path.join(settings.BASE_DIR, 'WaterMark','CICP_WaterMark.png')


USER_DESIGNATION_DICT = {'A' : 'pub', 'B' : 'prv', 'C' : 'chr'}

USER_DOMAIN_DICT = {    '1'	: 'Organizations Relieving Poverty',
                        '2'	: 'Foundations Relieving Poverty',
                        '10'	: 'Teaching Institutions',
                        '11'	: 'Support of schools and education',
                        '12'	: 'Education in the arts',
                        '13'	: 'Educational organizations not elsewhere categorized',
                        '14'	: 'Research',
                        '15'	: 'Foundations Advancing Education',
                        '30'	: 'Christianity',
                        '40'	: 'Islam',
                        '50'	: 'Judaism',
                        '60'	: 'Other Religions',
                        '70'	: 'Support of Religion',
                        '80'	: 'Ecumenical and Inter-faith Organizations',
                        '90'	: 'Foundations Advancing Religions',
                        '100'	: 'Core Health Care',
                        '110'	: 'Supportive Health Care',
                        '120'	: 'Protective Health Care',
                        '130'	: 'Health Care Products',
                        '140'	: 'Complementary or Alternative Health Care',
                        '150'	: 'Relief of the Aged',
                        '155'	: 'Upholding Human Rights',
                        '160'	: 'Community Resource',
                        '170'	: 'Environment',
                        '175'	: 'Agriculture',
                        '180'	: 'Animal Welfare',
                        '190'	: 'Arts',
                        '200'	: 'Public Amenities',
                        '210'	: 'Foundations',
                        '214'	: 'CAAA',
                        '215'	: 'NASO'}

USER_SUB_SAMPLE_IDS = [ 'SS1', 
                        'SS2', 
                        'SS3', 
                        'SS4',
                        'SS5',
                        'SS6', 
                        'SL Climate & Environment / Climat & Environnement', 
                        'SL Advocacy & Human rights / Plaidoyer et droits de l\'homme'
                        'SL Indigenous services / Services aux autochtones',
                        'SL Crisis Intervention / Intervention en cas de crise',
                        'SL Animal Welfare / Bien-Ãªtre des animaux',
                        'SL Literacy groups / Groupes d\'alphabÃ©tisation',
                        'SL Arts Education / Ã‰ducation artistique',
                        'SL Food Security / SÃ©curitÃ© alimentaire',
                        'SL Shelters / Organismes de refuge',
                        'SL Senior care / Soins aux personnes Ã¢gÃ©es',
                        'SL Humanitarian assistance (outside Canada) / Aide humanitaire (hors du Canada)',
                        'SL Migration services / Services de migration',
                        'Initial List',
                        
                        ]


##################################################################################################################################
# This dataClass contains all the values which the user wants to filter on
# it should be created by the viewer and passed to the controller
##################################################################################################################################

@dataclass
class FrontEndQuery:
    
    # Filter on Survey release data
    date: str = ''
    
    # Filter by survey ID
    # this filter is only used for the default image creation
    qualtricsSurveyID: str = ''
    
    # Filter on Question
    questionThemes: List = field(default_factory=lambda: [])  
    
    # Filter on User
    locations: List = field(default_factory=lambda: []) 
    organizationSizes: List = field(default_factory=lambda: []) 
    languagePreference: List = field(default_factory=lambda: []) 
    fieldOfWork: List = field(default_factory=lambda: [])       
                
    def IsDateOnly(self):
        
        isDateOnly = False
        
        if (len(self.questionThemes) == 0 and 
            len(self.locations) == 0 and 
            len(self.organizationSizes) == 0 and
            len(self.languagePreference) == 0 and
            len(self.fieldOfWork) == 0 and
            self.qualtricsSurveyID == ''):
                isDateOnly = True
        
        return isDateOnly
        
##################################################################################################################################
# This function changes a filepath local to the server to a url
##################################################################################################################################

def Local2URLMedia(listLocal):
    
    listOfURLPaths = []
    
    for localFilePath in listLocal:
        urlPath = localFilePath[len(str(settings.BASE_ROOT)):]
        listOfURLPaths.append(urlPath)
        
    return listOfURLPaths
    
    
##################################################################################################################################
# This function removes any text in brackets and replaces special characeter codes with the actual character
##################################################################################################################################


def CleanText(text):
    cleanedText = text
    cleanedText= cleanedText.replace("\n","")
    cleanedText = re.sub("[\[].*?[\]]", "", cleanedText)
    #cleanedText = re.sub("[\(].*?[\)]", "", cleanedText)
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
                tickLabels.append(fill(pairSplit[1],15)) 
            if len(pairSplit) == 3: 
                tickValues.append(float(pairSplit[1]))      
                tickLabels.append(fill(pairSplit[2],15)) 

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
def GetUser(externalRefNum, VERBOSE = False):
    
    userQuerySet = UserTable.objects.filter(externalDataReference=externalRefNum)
    user = None
    if len(userQuerySet) == 1:
        user = userQuerySet.first()      
    else:    
        if VERBOSE:
            print('[ERROR]: GetUser: No User found with:', externalRefNum)
        ##########################################################
        # Remove this could after development
        # replace it with code to handle a user doesnt exist
        user = UserTable()
        user.externalDataReference = externalRefNum
        user.province = 'AB'
        user.size = 'SM'
        user.domain = ''
        user.languagePreference = 'EN'
        user.save()
        ##########################################################
    
    return user

##################################################################################################################################
# 
##################################################################################################################################

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10
