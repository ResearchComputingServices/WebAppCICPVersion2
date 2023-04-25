from django.db.models import Q, QuerySet
import pandas as pd

import uuid

import warnings
warnings.filterwarnings('ignore')

from scripts.Utils import *
from scripts.DataVisualizer import DataVisualizerMain
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable

##################################################################################################################################
# 
##################################################################################################################################
def GetUserQuerySet(aQuery):
    userQuerySet = UserTable.objects.all()
        
    if len(aQuery.locations) != 0:
        qObject = Q()
        for loc in aQuery.locations:
            qObject |= Q(province=loc) 
        userQuerySet = userQuerySet.filter(qObject)
    
    if len(aQuery.organizationSizes) != 0: 
        qObject = Q()
        for size in aQuery.organizationSizes:
            qObject |= Q(size=size) 
        userQuerySet = userQuerySet.filter(qObject)
    
    if len(aQuery.languagePreference) != 0:        
        qObject = Q()
        for lang in aQuery.languagePreference:
            qObject |= Q(languagePreference=lang) 
        userQuerySet = userQuerySet.filter(qObject)
    
    if len(aQuery.fieldOfWork) != 0:
        qObject = Q()
        for work in aQuery.fieldOfWork:
            qObject |= Q(domain=work) 
        userQuerySet = userQuerySet.filter(qObject)
    
    if len(userQuerySet) < MINIMUM_USER_QUERY_SIZE:
        userQuerySet = None
    
    return userQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetSurveyQuerySet(aQuery):
    
    surveyQuerySet = SurveyTable.objects.all()
   

    if len(aQuery.date) != 0:
        surveyQuerySet = surveyQuerySet.filter(releaseDate=aQuery.date)
    
    if len(aQuery.qualtricsSurveyID) != 0:
        surveyQuerySet = surveyQuerySet.filter(qualtricsSurveyID=aQuery.qualtricsSurveyID)
           
    if len(surveyQuerySet) == 0:
        surveyQuerySet = None
                
    return surveyQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetQuestionQuerySet(aQuery):
    
    questionQuerySet = QuestionTable.objects.all()
   
    if len(aQuery.questionThemes) != 0:
        
        themeQueryObject = Q()
        
        for theme in aQuery.questionThemes:
            themeQueryObject |= Q(questionTheme=theme)
        
        questionQuerySet = questionQuerySet.filter(themeQueryObject)       
                  
    if len(questionQuerySet) == 0:
        questionQuerySet = None
          
    return questionQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetUserResponseQuerySet(aQuery, VERBOSE = False):
    
    # the data structure which will be returned
    userResponseQuerySet = None
    
    # this list will log any errors generated by the queries
    errorLogs = []
    
    # Get all the surveys that match the query
    surveyQuerySet = GetSurveyQuerySet(aQuery)
    # Get all questions that match the query
    questionQuerySet = GetQuestionQuerySet(aQuery)
    # Get all users that match the query
    userQuerySet = GetUserQuerySet(aQuery)
    
    if VERBOSE:
        if surveyQuerySet != None:
            print('surveyQuerySet',len(surveyQuerySet))
        else:
            print('surveyQuerySet is None')
        
        if questionQuerySet != None:
            print('questionQuerySet',len(questionQuerySet))
        else:
            print('questionQuerySet is None')
            
        if userQuerySet != None:
            print('userQuerySet',len(userQuerySet))
        else:
            print('userQuerySet is None')
            
    # test to make sure there is data in the querySets before proceeding
    if questionQuerySet != None and userQuerySet != None and surveyQuerySet != None:
        
        surveyQueryObject = Q()
        for s in surveyQuerySet:
            surveyQueryObject |= Q(surveyID=s.id)
          
        questionQuerySet = questionQuerySet.filter(surveyQueryObject)  
                   
        questionQueryObject = Q()
        for q in questionQuerySet:
            questionQueryObject |= Q(questionID=q.id)
    
        if len(questionQueryObject) != 0:
        
            userResponseQuerySet = UserResponseTable.objects.filter(questionQueryObject)
                    
            userQueryObject = Q()
            for u in userQuerySet:
                userQueryObject |= Q(userID = u.id)
              
            userResponseQuerySet = userResponseQuerySet.filter(userQueryObject)
    
            if len(userResponseQuerySet) == 0:
                if VERBOSE:
                    print('[ERROR]: GetUserQuerySet: no user responses fix query')
                errorLogs.append('Insufficient user response data, try relaxing search constraints')
        else:
            errorLogs.append('Insufficient question data')
            
    # if any of the querySets are zero report an error explaining why
    else:
        if questionQuerySet == None:
            if VERBOSE:
                print('[ERROR]: GetUserResponseQuerySet: Insufficient question data' )
            errorLogs.append('Insufficient question data, try relaxing search constraints')    
        if surveyQuerySet == None:
            if VERBOSE:
                print('[ERROR]: GetUserResponseQuerySet: Insufficient survey data' )    
            errorLogs.append('Insufficient survey data, try relaxing search constraints')
        if userQuerySet == None:
            if VERBOSE:
                print('[ERROR]: GetUserQuerySet: UserQuerySet below minimum threshold: ', MINIMUM_USER_QUERY_SIZE)
            errorLogs.append('Insufficient user data, try relaxing search constraints')
                 
    return userResponseQuerySet, errorLogs

##################################################################################################################################
# This function generates figures for all the questions in the current survey with no filtering of the data
##################################################################################################################################

def GenerateDefaultFigures(aSurvey):

    aQuery = FrontEndQuery()
    aQuery.qualtricsSurveyID = aSurvey.qualtricsSurveyID
    
    dateString =  aSurvey.releaseDate.strftime("%Y-%m-%d")
    saveToDirPath = os.path.join(DEFAULT_FIGURE_FOLDER_PATH, dateString)
       
    HandleFrontEndQuery(aQuery=aQuery,
                        saveToDirPath=saveToDirPath)
        
    return True
    
##################################################################################################################################
# 
##################################################################################################################################

def GenerateDataFile(responseDict,
                     saveToDirPath = TMP_FIGURE_FOLDER_PATH):
               
    dataFrameList = []
    
    for question in responseDict.keys():
        questiondDF = question.GetDataFileEntry()       
    
        userDataFrameList = []
        for user in responseDict[question]:
            userDF = user.GetDataFileEntry()
            
            userDataFrameList.append(userDF)
            
        userDF = pd.concat(userDataFrameList)       
        
        dataFrameList.append(pd.concat([questiondDF,userDF],axis=1))
    
    filePath = ''
    if len(dataFrameList) > 0:
        mainDataFrame = pd.concat(dataFrameList)   
        filename = str(uuid.uuid4()) + ".csv"
        filePath = os.path.join(saveToDirPath, filename)
        mainDataFrame.to_csv(filePath)
    
    return filePath


##################################################################################################################################
# This function returns a list of unique questions from the userResponse QuerySet generated by a frontend query
##################################################################################################################################
def GetListOfUniqueQuestions(userResponseQuerySet):
        questionList = []

        # Get all the unique questions in the set of responses

        #Priyanka
        if type(userResponseQuerySet) != str:
            questionIDs = userResponseQuerySet.order_by().values_list('questionID').distinct()

        # use the unique questionIDs to get a list of the questions

            if questionIDs:
                for qID in questionIDs:
                    questionQuerySet = QuestionTable.objects.filter(id=qID[0])
        
                    if len(questionQuerySet) == 1:
                        question = questionQuerySet.first()
        
                        # handle matrix questions differently because they have subQuestions    
                        if question.questionType == MATRIX_QUESTION:
                        
                            parentQuestion = QuestionTable.objects.filter(id=question.parentQuestionID.id).first()
        
                            if parentQuestion not in questionList:
                                questionList.append(parentQuestion) 
                        else:            
                            questionList.append(question)   
        
            return questionList

####    ##############################################################################################################################
# Th    is function returns a list responses to the question passed as an arguement
##################################################################################################################################

def GetUserResponsesToQuestion(question, userResponseQuerySet):
    
    userResponseList = []
    
    if question.questionType == MATRIX_QUESTION:
        subQuestionsQuerySet = QuestionTable.objects.filter(parentQuestionID=question.id)
        
        for subQuestion in subQuestionsQuerySet:
            responsesToQuestion = userResponseQuerySet.filter(questionID=subQuestion.id)
    
            for response in responsesToQuestion:
                userResponseList.append(response)
    else:
        responsesToQuestion = userResponseQuerySet.filter(questionID=question.id)
    
        for response in responsesToQuestion:
            userResponseList.append(response)
        
    return userResponseList

##################################################################################################################################
# 
##################################################################################################################################

def GetResponseDict(aQuery, VERBOSE = False):
    
    responseDict = {}
    userResponseQuerySet, errorLogs = GetUserResponseQuerySet(aQuery, VERBOSE)   
       
    if userResponseQuerySet != None:
   
        questionList = GetListOfUniqueQuestions(userResponseQuerySet)
        
        for question in questionList:   
            userResponseList = GetUserResponsesToQuestion(question, userResponseQuerySet)
            responseDict[question] = userResponseList
    
    return responseDict, errorLogs

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery, isEnglish = True, saveToDirPath = TMP_FIGURE_FOLDER_PATH):
     
    listOfImageFilePaths = []
    dataCSVFilePath = []
    errorLogs = []
    
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('HandleFrontEndQuery') 
    print('date:',aQuery.date)
    print('id',aQuery.qualtricsSurveyID)
    print('themes',aQuery.questionThemes)
    print('location',aQuery.locations)
    print('size',aQuery.organizationSizes)
    print('lang',aQuery.languagePreference)
    print('field',aQuery.fieldOfWork)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    # If only a date is specified in the query then no new images need to be generated since the default
    # images created when then the survey data was pulled from the website fullfill the request.
    if aQuery.IsDateOnly():  
        print('QueryType: Date Only Query')

        folderPath = os.path.join(DEFAULT_FIGURE_FOLDER_PATH, aQuery.date)
        print('FolderPath:', folderPath)

        if os.path.exists(folderPath):
            for filename in os.listdir(folderPath):
                if os.path.isfile(os.path.join(folderPath, filename)):

                    filePath = os.path.join(folderPath, filename)
                                        
                    if '.csv' in filename:    
                        dataCSVFilePath.append(filePath)
                    else:
                        listOfImageFilePaths.append(filePath)   
        else:
            print("[WARNING]: HandleFrontEndQuery: Folder path doesn't exist:", folderPath)     
    # If there are more filters in the query then just a date, new images will need to be generated.
    else: 
        print('QueryType: Full Query')
         
        responseDict, errorLogs = GetResponseDict(aQuery, True)
        
        if responseDict.keys() != None:
            listOfImageFilePaths = DataVisualizerMain(responseDict, isEnglish, saveToDirPath)                                  
            dataCSVFilePath = ""#GenerateDataFile(responseDict, saveToDirPath)
    
    listOfImageFilePaths = Local2URLMedia(listOfImageFilePaths)
    dataCSVFilePath = Local2URLMedia([dataCSVFilePath])    
      
    print('Generated Images Location:')
    print(listOfImageFilePaths)
    
    return listOfImageFilePaths, dataCSVFilePath, errorLogs
    
##################################################################################################################################
# This function is used to test the controller functions
##################################################################################################################################
def run(*arg):    
    
    aQuery = FrontEndQuery()   
    aQuery.qualtricsSurveyID = 'SV_0eMEVIZkeSbKyjk'#'SV_6mJwD0WeUarScKy'
    aQuery.locations = ["ON"]
    images, data, errorLogs = HandleFrontEndQuery(aQuery) 

    print('~~~~~~~~~~ QUERY ERROR LOG ~~~~~~~~~~')
    for error in errorLogs:
        print(error)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    print('~~~~~~~~~~~ IMAGE OUTPUTS ~~~~~~~~~~~')
    print(images)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    
    print('~~~~~~~~~~~ DATA  OUTPUTS ~~~~~~~~~~~')
    print(data)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    input('Press Enter to continue...')
