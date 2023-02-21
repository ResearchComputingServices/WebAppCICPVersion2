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
    
    if len(userQuerySet) == 0:
        userQuerySet = None
        print('[ERROR]: GetUserQuerySet: UserQuerySet size is 0')
    elif len(userQuerySet) < MINIMUM_USER_QUERY_SIZE:
        print('[ERROR]: GetUserQuerySet: UserQuerySet below minimum threshold: ', len(userQuerySet), '<', MINIMUM_USER_QUERY_SIZE)
  
    return userQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetSurveyQuerySet(aQuery):
    
    surveyQuerySet = SurveyTable.objects.all()

    print(len(surveyQuerySet))

    if len(aQuery.date) != 0:
        surveyQuerySet = surveyQuerySet.filter(releaseDate=aQuery.date)
    
    print(len(surveyQuerySet))
    
    if len(aQuery.qualtricsSurveyID) != 0:
        surveyQuerySet = surveyQuerySet.filter(qualtricsSurveyID=aQuery.qualtricsSurveyID)
           
    print(len(surveyQuerySet))

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
def GetUserResponseQuerySet(aQuery):
    
    # the data structure which will be returned
    userResponseQuerySet = None
    
    # Get all the surveys that match the query
    surveyQuerySet = GetSurveyQuerySet(aQuery)
                
    # Get all questions that match the query
    questionQuerySet = GetQuestionQuerySet(aQuery)
           
    # Get all users that match the query
    userQuerySet = GetUserQuerySet(aQuery)
    
    if  surveyQuerySet != None:
        print('Survey:', len(surveyQuerySet))
    else:
        print(0)     
        
    if  questionQuerySet != None:
        print('Questions:', len(questionQuerySet))
    else:
        print(0)     
              
    if userQuerySet != None:
        print('User:', len(userQuerySet))
    else:
        print(0)     
        
    if questionQuerySet != None and userQuerySet != None and surveyQuerySet != None:
            
        surveyQueryObject = Q()
        for s in surveyQuerySet:
            surveyQueryObject |= Q(surveyID=s.id)
          
        questionQuerySet = questionQuerySet.filter(surveyQueryObject)  
                   
        questionQueryObject = Q()
        for q in questionQuerySet:
            questionQueryObject |= Q(questionID=q.id)
        
        userResponseQuerySet = UserResponseTable.objects.filter(questionQueryObject)
                 
        userQueryObject = Q()
        for u in userQuerySet:
            userQueryObject |= Q(userID = u.id)
        
        userResponseQuerySet = userResponseQuerySet.filter(userQueryObject)
    else:
        print('[ERROR]: GetUserResponseQuerySet: Insufficient question or user data' )
    
               
    return userResponseQuerySet

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
                     saveToDirPath = FIGURE_FOLDER_PATH):
               
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

##################################################################################################################################
# This function returns a list responses to the question passed as an arguement
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

def GetResponseDict(aQuery):
    
    responseDict = {}
    userResponseQuerySet = GetUserResponseQuerySet(aQuery)   
    
    if userResponseQuerySet != None:
   
        questionList = GetListOfUniqueQuestions(userResponseQuerySet)
        
        for question in questionList:   
            userResponseList = GetUserResponsesToQuestion(question, userResponseQuerySet)
            responseDict[question] = userResponseList
    
    return responseDict

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery, isEnglish = True, saveToDirPath = FIGURE_FOLDER_PATH):
     
    listOfImageFilePaths = []
    dataCSVFilePath = []
      
    if aQuery.IsDateOnly() and False:
        
        folderPath = os.path.join(DEFAULT_FIGURE_FOLDER_PATH, aQuery.date)
    
        if os.path.exists(folderPath):
            for filename in os.listdir(folderPath):
                if os.path.isfile(os.path.join(folderPath, filename)):
                    
                    filePath = os.path.join(folderPath, filename)
                    
                    if '.csv' in filename:    
                        dataCSVFilePath.append(filePath)
                    else:
                        listOfImageFilePaths.append(filePath)            
    else:       
        responseDict = GetResponseDict(aQuery)
        
        if responseDict.keys() != None:
            listOfImageFilePaths = DataVisualizerMain(responseDict, isEnglish, saveToDirPath)                                  
            dataCSVFilePath = GenerateDataFile(responseDict, saveToDirPath)
        else:
            print('[WARNING]: HandleFrontEndQuery: Insufficient data available for selected query')
    
    return listOfImageFilePaths, dataCSVFilePath
    
##################################################################################################################################
# This function is used to test the controller functions
##################################################################################################################################
def run(*arg):

    aQuery = None
    if len(arg) == 0:
        # dateList = ['2022-12-01','2022-12-08','2022-12-17','2023-02-03','2023-02-01','2023-01-01']
        dateList = ['2022-12-17']
        for date in dateList:
            aQuery = FrontEndQuery()   
            #aQuery.date = date
            #aQuery.qualtricsSurveyID = 'SV_aYnUZN7y2nQhXJc'
            aQuery.questionThemes = ['GOV']
            
            aQuery.organizationSizes = ['MEDIUM']
            aQuery.locations = ['NL']
            aQuery.languagePreference = ['FR']
          
            images, data = HandleFrontEndQuery(aQuery) 

            print(images)
            print(data)

            input('Press Enter to continue...')

    else:
        aQuery = arg[0]
        return HandleFrontEndQuery(aQuery)    