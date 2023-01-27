from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from dataclasses import dataclass, field
from typing import List, Dict

##################################################################################################################################
# 
##################################################################################################################################

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
                                'Consent',
                                'ExternalDataReference']

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
