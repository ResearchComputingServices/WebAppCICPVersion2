from scripts.Utils import *
from InteractiveDB.models import SurveyTable

from scripts.Controller import GenerateDefaultFigures



def run(*args):
    
    surveyQuerySet = SurveyTable.objects.all()

    for survey in surveyQuerySet:
        print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)
        #print('ExtractSurveyMain')
        #ExtractSurveyMain(aSurvey=survey)

        #print('ExtractResponsesMain')
        #ExtractResponsesMain(aSurvey=survey)

        print('GenerateDefaultFigures')
        GenerateDefaultFigures(aSurvey=survey) 