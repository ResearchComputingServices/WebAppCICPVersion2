from django.db.models import Q
import pandas as pd
from datetime import date, datetime
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
        userQuerySet = userQuerySet.filter(province=aQuery.locations)

    
    if len(aQuery.organizationSizes) != 0:
        userQuerySet = userQuerySet.filter(size=aQuery.organizationSizes)
  
    
    if len(aQuery.languagePreference) != 0:
        userQuerySet = userQuerySet.filter(languagePreference=aQuery.languagePreference)
  
        
    if len(aQuery.fieldOfWork) != 0:
        userQuerySet = userQuerySet.filter(domain=aQuery.fieldOfWork)
  
    return userQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetQuestionQuerySet(aQuery):
    
    questionQuerySet = QuestionTable.objects.all()
    surveyQuerySet = SurveyTable.objects.all()
       
    if aQuery.date != None:
        surveyQuerySet = surveyQuerySet.filter(releaseDate=aQuery.date)
    
    if len(aQuery.questionThemes) != 0:
        questionQuerySet = questionQuerySet.filter(questionTheme=aQuery.questionThemes)
        
    qObject = Q()
    for e in surveyQuerySet:
        qObject |= Q(surveyID=e.id)
      
    questionQuerySet = questionQuerySet.filter(qObject)
      
    return questionQuerySet

##################################################################################################################################
# 
##################################################################################################################################
def GetUserResponseQuerySet(aQuery):
    # Get all questions that match the query
    questionQuerySet = GetQuestionQuerySet(aQuery)
    
    # Get all users that match the query
    userQuerySet = GetUserQuerySet(aQuery)
    
    # Create a queryObject that concatenates both user and questios with OR operations   
    quereObject = Q()
    for q in questionQuerySet:
        for u in userQuerySet:
            quereObject |= Q(questionID=q.id, userID = u.id)
    
    # Get all the userResponses that match the queryObject
    userResponseQuerySet = UserResponseTable.objects.filter(quereObject)
    
    return userResponseQuerySet

##################################################################################################################################
# This function generates figures for all the questions in the current survey with no filtering of the data
##################################################################################################################################

def GenerateDefaultFigures(aSurvey):

    aQuery = FrontEndQuery()   
    aQuery.date = aSurvey.releaseDate
    
    dateString =  aSurvey.releaseDate.strftime("%d-%m-%Y")
    
    saveToDirPath = os.path.join(DEFAULT_FIGURE_FOLDER_PATH, dateString)
       
    listOfImageFilePaths, dataCSVFilePath = HandleFrontEndQuery(aQuery=aQuery,
                                                                saveToDirPath=saveToDirPath)
        
    return True
    
##################################################################################################################################
# 
##################################################################################################################################

def GenerateDataFile(userResponseQuerySet,
                     saveToDirPath = FIGURE_FOLDER_PATH):
            
    mainDataFrame = pd.DataFrame()
    
    for user in userResponseQuerySet:
        entryDict = user.GetDataFileEntry()
        
        if len(mainDataFrame.index) != 0:
            mainDataFrame = mainDataFrame.append(entryDict,ignore_index=True)
        else:
            mainDataFrame = pd.DataFrame(entryDict, index=[0])
        
    filename = str(uuid.uuid4()) + ".csv"
    figureFilePath = os.path.join(saveToDirPath, filename)

    mainDataFrame.to_csv(figureFilePath)
    
    return figureFilePath

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery, isEnglish = True, saveToDirPath = FIGURE_FOLDER_PATH):
       
    userResponseQuerySet = GetUserResponseQuerySet(aQuery)
    
    listOfImageFilePaths = DataVisualizerMain(userResponseQuerySet, isEnglish, saveToDirPath)
    
    dataCSVFilePath = GenerateDataFile(userResponseQuerySet, saveToDirPath)
    
    return listOfImageFilePaths, dataCSVFilePath
    
##################################################################################################################################
# This function is used to test the controller functions
##################################################################################################################################
def run(*arg):

    aQuery = None
    if len(arg) == 0:
        dateList = ['2022-12-01','2022-12-02','2022-12-03','2022-12-04','2022-12-05','2022-12-06']
    
        for date in dateList:
            aQuery = FrontEndQuery()   
            aQuery.date = date
            aQuery.locations = 'AB'
           
            HandleFrontEndQuery(aQuery) 
    else:
        aQuery = arg[0]
        return HandleFrontEndQuery(aQuery)    