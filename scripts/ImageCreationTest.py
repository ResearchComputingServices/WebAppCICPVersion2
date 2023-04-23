from scripts.Utils import *
from InteractiveDB.models import SurveyTable

from scripts.Controller import GenerateDefaultFigures



def run(*args):
    
    surveyQuerySet = SurveyTable.objects.all()

    for survey in surveyQuerySet:
        #print('ExtractSurveyMain')
        #ExtractSurveyMain(aSurvey=survey)

        #print('ExtractResponsesMain')
        #ExtractResponsesMain(aSurvey=survey)

        if survey.qualtricsSurveyID == 'SV_4PKhCR2n0Hw6xbo':
            print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)
            print('GenerateDefaultFigures') 
            GenerateDefaultFigures(aSurvey=survey) 