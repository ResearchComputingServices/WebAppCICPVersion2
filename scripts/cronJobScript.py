from WebAppCICPVersion2 import settings
from scripts.Utils import *
from InteractiveDB.models import SurveyTable
from datetime import date, datetime

from scripts.FetchData import FetchDataMain
from scripts.ExtractSurvey import ExtractSurveyMain
from scripts.ExtractResponses import ExtractResponsesMain

##################################################################################################################################
# Main function 
##################################################################################################################################
def HandleReleasedSurvey(currentSurvey, currentDate):
    successFlag = False

    print('Download data for survey:',currentSurvey.qualtricsSurveyID)
    FetchDataMain(aSurvey=currentSurvey)
    
    print('ExtractSurveyMain')
    successFlag = ExtractSurveyMain(aSurvey=currentSurvey)
    
    print('ExtractResponsesMain')
    successFlag = ExtractResponsesMain(aSurvey=currentSurvey)
    
    if successFlag:
        currentSurvey.accessedDate = currentDate
        currentSurvey.save()
    else:
        print('[ERROR]: HandleReleasedSurvey: Unable to retrieve survey:', currentSurvey.qualtricsSurveyID)

##################################################################################################################################
# Main function 
# - this function will be called periodically by the cronJob
# - it will query the database for all the surveys then Fetch and Extract all those for which the releaseData field has passed
#   and which do not have an accessedDate field defined.
# - after Fetching and Extracting the survey entities accessedDate field will be set to the current date
################################################################################################################################## 
def AddSurvey(id,date):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.save()


def run(*args):
    ##########################################################
    # TODO: Remove this block before production!
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2022-12-01')
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-17')
    AddSurvey('SV_0eMEVIZkeSbKyjk','2023-01-03')
    ##########################################################
    
    surveyQuerySet = SurveyTable.objects.all()
    
    currentDate = date.today()
    
    print(currentDate)
    
    for survey in surveyQuerySet:
        print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.accessedDate)
        
        if currentDate >= survey.releaseDate:
            HandleReleasedSurvey(survey,currentDate)
        else:
            print('skip survey')