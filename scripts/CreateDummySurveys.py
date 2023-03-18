from InteractiveDB.models import SurveyTable

def AddSurvey(id,date):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.save()

def run(*args):
    #########################################################
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-07')
    # AddSurvey('SV_0eMEVIZkeSbKyjk','2022-12-14')
    # AddSurvey('SV_4PKhCR2n0Hw6xbo','2023-01-04')
    # AddSurvey('SV_8D2MdCYlLUZqu22','2023-01-11')
    # AddSurvey('SV_0SqKvaglCv3ophA','2023-01-18')
    # AddSurvey('SV_4U8obsyEzkfvxTE','2023-01-25')
    # AddSurvey('SV_aaZ43Vpy5PrPBjg','2023-02-01')
    # AddSurvey('SV_0BRc1sj0ALgtxmC','2023-02-08')
    # AddSurvey('SV_cSUrXPI6VggGvEq','2023-02-15')
    # AddSurvey('SV_42rjmguCfnl7s7s','2023-02-22')
    # AddSurvey('SV_6nk4KaDYWIazwSq','2023-03-01')
    # AddSurvey('SV_9Kpc8ttIoJCDwhg','2023-03-08')
    #########################################################

