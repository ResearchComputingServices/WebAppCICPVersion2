from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

dataDirPath = 'Data'
questionEnglishJSONFileName = 'surveyQuestionsEnglish.json'
questionFrenchJSONFileName = 'surveyQuestionsFrench.json'
responseDataJSONFileName = 'responseFile.json'


# ToDo: change this to automatically connect the corret base directory
baseDir = '/home/nickshiell/Documents/WebAppCICP/WebAppCICP'

RESPONSE_KEYS_TO_REMOVE_LIST = ['ResponseID',
                                'ResponseSet',
                                'IPAddress',
                                'StartDate',
                                'EndDate',
                                'RecipientLastName',
                                'RecipientFirstName',
                                'RecipientEmail',
                                'Finished',
                                'Status',
                                'LocationLatitude',
                                'LocationLongitude',
                                'LocationAccuracy',
                                'Consent',
                                'ExternalDataReference']

#TEST_SURVEY_ID = "SV_8epSb35vMSlpwea"
TEST_SURVEY_ID = "SV_4PKhCR2n0Hw6xbo"
#TEST_SURVEY_ID = "SV_aYnUZN7y2nQhXJc" # PASS
#TEST_SURVEY_ID = 'SV_0eMEVIZkeSbKyjk' # PASS

##################################################################################################################################
# 
##################################################################################################################################
def GetQuestion(surveyID,questionName):
    questionQuerySet = QuestionTable.objects.filter(surveyID=surveyID, questionName=questionName)
        
    if len(questionQuerySet) == 1:
        return questionQuerySet.first()
    else:
        print('[ERROR]: questionName is not unique: ', surveyID, questionName)

##################################################################################################################################
# 
##################################################################################################################################
def GetSurveyQuestionsFromDB(qualtricsSurveyID):
    survey = SurveyTable.objects.filter(qualtricsSurveyID=qualtricsSurveyID).first()
    surveyQuestions = QuestionTable.objects.filter(surveyID=survey.surveyID) 

    return surveyQuestions

##################################################################################################################################
# 
##################################################################################################################################
def GetSurveyID(qualtricSurveyID):
    surveyQuerySet = SurveyTable.objects.filter(qualtricsSurveyID=qualtricSurveyID)
    
    surveyID = -1
    
    if len(surveyQuerySet) == 1:
        surveyID = surveyQuerySet.first().surveyID
    else:
        print('[ERROR]: qualtricsSurveyID is not unique: ', qualtricSurveyID, len(surveyQuerySet))
    
    return surveyID