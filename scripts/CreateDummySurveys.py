from InteractiveDB.models import SurveyTable

def AddSurvey(id,date):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.save()

def run(*args):
    #########################################################
    #AddSurvey('SV_8epSb35vMSlpwea','2022-12-01')    # Sample Survey
    AddSurvey('SV_4PKhCR2n0Hw6xbo','2022-12-08')
    AddSurvey('SV_aYnUZN7y2nQhXJc','2022-12-17')
    AddSurvey('SV_0eMEVIZkeSbKyjk','2023-02-03')
    AddSurvey('SV_dhjlzfTnCj7mwT4','2023-02-01')
    AddSurvey('SV_6mJwD0WeUarScKy','2023-01-01')
    #########################################################

