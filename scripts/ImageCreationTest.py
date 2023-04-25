from scripts.Utils import *
from InteractiveDB.models import SurveyTable

from scripts.Controller import GenerateDefaultFigures



def run(*args):
    
    surveyQuerySet = SurveyTable.objects.all()

    # doneList = ['SV_aYnUZN7y2nQhXJc',
    #             'SV_0eMEVIZkeSbKyjk',
    #             'SV_4PKhCR2n0Hw6xbo',
    #             'SV_8D2MdCYlLUZqu22', 
    #             'SV_0SqKvaglCv3ophA',
    #             'SV_3agBieQhc6t7d2K',
    #             'SV_dhjlzfTnCj7mwT4',
    #             'SV_1RnShmHTBkbGhCu',
    #             'SV_cSUrXPI6VggGvEq',
    #             'SV_42rjmguCfnl7s7s',
    #             'SV_6nk4KaDYWIazwSq',
    #             'SV_9Kpc8ttIoJCDwhg',
    #             'SV_4ONclMGWEiBoZFk',
    #             'SV_29xoxQFVl4Rladg',
    #             'SV_55fMnaZIQKk86ZE']
    
    doneList = ['SV_aYnUZN7y2nQhXJc',
                'SV_0eMEVIZkeSbKyjk']

    for survey in surveyQuerySet:
        
        if survey.qualtricsSurveyID in doneList:
            continue
        else:            
                print(survey.id,'\n',survey.qualtricsSurveyID,'\n',survey.releaseDate,'\n',survey.fetchedDate)
                print('GenerateDefaultFigures') 
                GenerateDefaultFigures(aSurvey=survey) 
                input('Press ENTER to Continue...')