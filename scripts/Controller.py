from django.db.models import Q
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
# 
##################################################################################################################################

def GenerateDataFile(userResponseQuerySet):
            
    mainDataFrame = pd.DataFrame()
    
    for user in userResponseQuerySet:
        entryDict = user.GetDataFileEntry()
        
        if len(mainDataFrame.index) != 0:
            mainDataFrame = mainDataFrame.append(entryDict,ignore_index=True)
        else:
            mainDataFrame = pd.DataFrame(entryDict, index=[0])
        
    filename = str(uuid.uuid4())
    figureFilePath = os.path.join(FIGURE_FOLDER_PATH, filename)

    mainDataFrame.to_csv(figureFilePath)

##################################################################################################################################
# 
##################################################################################################################################

def HandleFrontEndQuery(aQuery):
    
    userResponseQuerySet = GetUserResponseQuerySet(aQuery)
    
    listOfImageFilePaths = DataVisualizerMain(userResponseQuerySet)
    
    dataCSVFilePath = GenerateDataFile(userResponseQuerySet)
    
    return listOfImageFilePaths, dataCSVFilePath
    
##################################################################################################################################
# This function is used to test the controller functions
##################################################################################################################################
def run(*arg):
    aQuery = FrontEndQuery()   
    aQuery.date = '2023-01-03'
    aQuery.locations = 'AB'

    userResponseQuerySet = GetUserResponseQuerySet(aQuery)
   
    GenerateDataFile(userResponseQuerySet)
    
    # print('# of responses found:', len(userResponseQuerySet))
    
    # for userResponse in userResponseQuerySet:
    #     print(userResponse)
    #     input()