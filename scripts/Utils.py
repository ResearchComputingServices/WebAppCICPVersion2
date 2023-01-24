from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

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