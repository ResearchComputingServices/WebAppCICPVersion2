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
def GetQuestion(aSurvey,questionName):
    
    questionQuerySet = QuestionTable.objects.filter(surveyID=aSurvey, questionName=questionName)
        
    if len(questionQuerySet) == 1:
        return questionQuerySet.first()
    else:
        print('[ERROR]: GetQuestion: questionName is not unique: ', aSurvey, questionName)

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
def GetSurvey(qualtricSurveyID):
    surveyQuerySet = SurveyTable.objects.filter(qualtricsSurveyID=qualtricSurveyID)
    
    survey = None
    if len(surveyQuerySet) == 1:
        survey = surveyQuerySet.first()
    else:
        print('[ERROR]: GetSurvey: qualtricsSurveyID is not unique: ', qualtricSurveyID, len(surveyQuerySet))
    
    return survey