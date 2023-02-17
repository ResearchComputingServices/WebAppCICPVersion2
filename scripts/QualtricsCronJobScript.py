from WebAppCICPVersion2 import settings
from scripts.Utils import *
from InteractiveDB.models import SurveyTable
from datetime import date

from scripts.FetchData import FetchDataMain
from scripts.ExtractSurvey import ExtractSurveyMain
from scripts.ExtractResponses import ExtractResponsesMain
from scripts.Controller import GenerateDefaultFigures

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
    
    print('GenerateDefaultFigures')
    successFlag = GenerateDefaultFigures(aSurvey=currentSurvey) 
        
    if successFlag:
        currentSurvey.fetchedDate = currentDate
        currentSurvey.save()
    else:
        print('[ERROR]: HandleReleasedSurvey: Unable to retrieve survey:', currentSurvey.qualtricsSurveyID)

##################################################################################################################################
# Main function 
# - this function will be called periodically by the cronJob
# - it will query the database for all the surveys then Fetch and Extract all those for which the releaseData field has passed
#   and which do not have an fetchedDate field defined.
# - after Fetching and Extracting the survey entities fetchedDate field will be set to the current date
################################################################################################################################## 
def AddSurvey(id,date):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.save()

def run(*args):
    ##########################################################
    # TODO: Remove this block before production!
    # Remove comments below to test this script
    # AddSurvey('SV_8epSb35vMSlpwea','2022-12-01')    # Sample Survey
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2022-12-08')
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-17')
    AddSurvey('SV_0eMEVIZkeSbKyjk','2023-02-03')
    AddSurvey('SV_dhjlzfTnCj7mwT4','2023-02-01')
    AddSurvey('SV_6mJwD0WeUarScKy','2023-01-01')
    # #########################################################
    
    surveyQuerySet = SurveyTable.objects.all()
    
    currentDate = date.today()
    
    print(currentDate)
    
    for survey in surveyQuerySet:
        print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)
        
        if currentDate >= survey.releaseDate and survey.fetchedDate == None:
            HandleReleasedSurvey(survey,currentDate)
        else:
            print('skip survey')