from InteractiveDB.models import SurveyTable

def AddSurvey(id,date,theme):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.surveyTheme = theme
    survey.save()

def run(*args):
    
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-07','CHA') 
    AddSurvey('SV_0eMEVIZkeSbKyjk','2022-12-14','CHA')
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2023-01-04','OTH') 
    AddSurvey('SV_8D2MdCYlLUZqu22','2023-01-11','GOV')
    AddSurvey('SV_0SqKvaglCv3ophA','2023-01-18','EDI')
    AddSurvey('SV_3agBieQhc6t7d2K','2023-01-25','FUN')
    AddSurvey('SV_dhjlzfTnCj7mwT4','2023-02-01','GOV') 
    AddSurvey('SV_1RnShmHTBkbGhCu','2023-02-08','COL') 
    AddSurvey('SV_cSUrXPI6VggGvEq','2023-02-15','POL')
    AddSurvey('SV_42rjmguCfnl7s7s','2023-02-22','EDI')
    AddSurvey('SV_6nk4KaDYWIazwSq','2023-03-01','GOV')
    AddSurvey('SV_9Kpc8ttIoJCDwhg','2023-03-08','OTH')
    AddSurvey('SV_4ONclMGWEiBoZFk','2023-03-15','FUN')
    AddSurvey('SV_29xoxQFVl4Rladg','2023-03-22','OTH') 
    AddSurvey('SV_55fMnaZIQKk86ZE','2023-03-29','CHA') 
    AddSurvey('SV_1QRGU5FIfrMVtKm','2023-04-05','CHA')
    AddSurvey('SV_6DTO78p2MVG52g6','2023-04-12','GOV')
    AddSurvey('SV_cPlOlLZZhtASd5I','2023-04-19','COL')
    AddSurvey('SV_8CzGXW2wXTMn9gq','2023-04-26','POL')
    AddSurvey('SV_0lJ2ddSC0PnAQPI','2023-05-03','CHA')
    AddSurvey('SV_bqKBmSENlLRWNWm','2023-05-10','FUN')
    AddSurvey('SV_1ziHebaCSozfbRc','2023-05-17','EDI')
    AddSurvey('SV_8emOMKK68Ne2JIW','2023-05-24','GOV')
    AddSurvey('SV_e3fX4mMxLUEMXS6','2023-05-31','OTH')
    AddSurvey('SV_dbY9Vbg47dMKEwS','2023-06-07','GOV')
    AddSurvey('SV_cVfK6cKOue4VZgW','2023-06-14','FUN')
    AddSurvey('SV_bC479yMxWekXnWS','2023-06-21','GOV')
    AddSurvey('SV_bycpZWVyBjTlmSO','2023-06-28','POL')
    AddSurvey('SV_0xsnw9eASP8WJYW','2023-07-05','CHA')
    AddSurvey('SV_3L4rLLzhPt3qx7g','2023-07-12','CHA')
    # AddSurvey('SV_5zn42gF56T58USy','2023-07-19','EDI')

