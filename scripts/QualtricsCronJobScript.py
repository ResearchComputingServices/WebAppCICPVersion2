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
    # successFlag = True

    print('Download data for survey:',currentSurvey.qualtricsSurveyID)
    successFlag = FetchDataMain(aSurvey=currentSurvey)
    
    if successFlag:
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

    else:
        print('[ERROR]: HandleReleasedSurvey: Unable to download survey data :', currentSurvey.qualtricsSurveyID)

##################################################################################################################################
# Main function 
# - this function will be called periodically by the cronJob
# - it will query the database for all the surveys then Fetch and Extract all those for which the releaseData field has passed
#   and which do not have an fetchedDate field defined.
# - after Fetching and Extracting the survey entities fetchedDate field will be set to the current date
################################################################################################################################## 
def run(*args):
    
    surveyQuerySet = SurveyTable.objects.all()
    
    currentDate = date.today()
        
    for survey in surveyQuerySet:
        print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)
        
        if currentDate >= survey.releaseDate and survey.surveyTheme != "NULL" and survey.fetchedDate == None:
            HandleReleasedSurvey(survey,currentDate)
        else:
            print('skip survey')
