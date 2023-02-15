from django.db.models import Q, QuerySet
import pandas as pd
from datetime import date, datetime
import uuid
import time

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
  
    return userQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetQuestionQuerySet(aQuery):
    
    surveyQuerySet = SurveyTable.objects.all()

    if aQuery.date != None:
        surveyQuerySet = surveyQuerySet.filter(releaseDate=aQuery.date)
        
    if aQuery.qualtricsSurveyID != None:
        surveyQuerySet = surveyQuerySet.filter(qualtricsSurveyID=aQuery.qualtricsSurveyID)
                
    if len(aQuery.questionThemes) != 0:
        questionQuerySet = questionQuerySet.filter(questionTheme=aQuery.questionThemes)
    
    questionQuerySet = None
    if len(surveyQuerySet) != 0:    
        qObject = Q()
        for e in surveyQuerySet:
            qObject |= Q(surveyID=e.id)
      
        questionQuerySet = QuestionTable.objects.filter(qObject)
     
    return questionQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetUserResponseQuerySet(aQuery):
    
    # the data structure which will be returned
    userResponseQuerySet = None
    
    # Get all questions that match the query
    questionQuerySet = GetQuestionQuerySet(aQuery)
    
    # Get all users that match the query
    userQuerySet = GetUserQuerySet(aQuery)
             
    if questionQuerySet != None and userQuerySet != None:
        
        # Create a queryObject that concatenates both userID and questionID with OR operators   
        questionQueryObject = Q()
        for q in questionQuerySet:
            questionQueryObject |= Q(questionID=q.id)
        
        userResponseQuerySet = UserResponseTable.objects.filter(questionQueryObject)
     
        userQueryObject = Q()
        for u in userQuerySet:
            userQueryObject |= Q(userID = u.id)
        
        userResponseQuerySet = userResponseQuerySet.filter(userQueryObject)
            
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

def GenerateDataFile(userResponseQuerySet,
                     saveToDirPath = FIGURE_FOLDER_PATH):
            
    mainDataFrame = pd.DataFrame()
    
    s1 = time.time()
    for user in userResponseQuerySet:
        entryDict = user.GetDataFileEntry()
       
        if len(mainDataFrame.index) != 0:
            mainDataFrame = mainDataFrame.append(entryDict,ignore_index=True)
        else:
            mainDataFrame = pd.DataFrame(entryDict, index=[0])
            
    e1 = time.time()
    print('for-loop:', e1 - s1)
    
    filename = str(uuid.uuid4()) + ".csv"
    figureFilePath = os.path.join(saveToDirPath, filename)
    mainDataFrame.to_csv(figureFilePath)
    
    return figureFilePath

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery, isEnglish = True, saveToDirPath = FIGURE_FOLDER_PATH):
     
    listOfImageFilePaths = []
    dataCSVFilePath = []
      
    if aQuery.IsDateOnly():
        
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
        print('GetUserResponseQuerySet')
        userResponseQuerySet = GetUserResponseQuerySet(aQuery)
        
        if userResponseQuerySet != None:
            print('DataVisualizerMain')
            s0 = time.time()
            listOfImageFilePaths = DataVisualizerMain(userResponseQuerySet, isEnglish, saveToDirPath)   
            e0 = time.time()
            print('DataVisualizerMain', e0 - s0)
            
            
            print('GenerateDataFile')
            s1 = time.time()    
            dataCSVFilePath = GenerateDataFile(userResponseQuerySet, saveToDirPath)
            e1 = time.time()
            print('GenerateDataFile: ', e1 -s1)
        
        else:
            print('[WARNING]: HandleFrontEndQuery: No data available for selected query')
    
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
            aQuery.date = date
            aQuery.organizationSizes = ['small','medium','large']
          
            images, data = HandleFrontEndQuery(aQuery) 

            print(images)
            print(data)

            input()

    else:
        aQuery = arg[0]
        return HandleFrontEndQuery(aQuery)    