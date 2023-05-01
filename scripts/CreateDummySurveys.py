from InteractiveDB.models import SurveyTable

def AddSurvey(id,date):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.save()

def run(*args):
    
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-07') 
    AddSurvey('SV_0eMEVIZkeSbKyjk','2022-12-14')
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2023-01-04') 
    AddSurvey('SV_8D2MdCYlLUZqu22','2023-01-11')
    AddSurvey('SV_0SqKvaglCv3ophA','2023-01-18')
    AddSurvey('SV_3agBieQhc6t7d2K','2023-01-25')
    AddSurvey('SV_dhjlzfTnCj7mwT4','2023-02-01') # ERROR
    AddSurvey('SV_1RnShmHTBkbGhCu','2023-02-08') # ERROR
    AddSurvey('SV_cSUrXPI6VggGvEq','2023-02-15')
    AddSurvey('SV_42rjmguCfnl7s7s','2023-02-22')
    AddSurvey('SV_6nk4KaDYWIazwSq','2023-03-01')
    AddSurvey('SV_9Kpc8ttIoJCDwhg','2023-03-08')
    AddSurvey('SV_4ONclMGWEiBoZFk','2023-03-15')
    AddSurvey('SV_29xoxQFVl4Rladg','2023-03-22') 
    AddSurvey('SV_55fMnaZIQKk86ZE','2023-03-29') 
    AddSurvey('SV_1QRGU5FIfrMVtKm','2023-04-05')
    AddSurvey('SV_6DTO78p2MVG52g6','2023-04-12')
    AddSurvey('SV_cPlOlLZZhtASd5I','2023-04-19')
