import requests
import zipfile
import io
import os
import json
import math
import pandas as pd

from scripts.Utils import *
from WebAppCICPVersion2 import settings

##################################################################################################################################
# This function fetchs the survey question data from the Qualtric website and saves the fetched information into a JSON file
##################################################################################################################################
def FetchSurveyQuestionsJSON(   surveyID,
                                outputFilePath):
    # Setting user Parameters   
    apiToken = settings.QUATRICS_API['api_token']
    dataCenter = settings.QUATRICS_API['data_center']

    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}".format(dataCenter, surveyID)
    headers = {"x-api-token": apiToken,}
    
    response = requests.get(baseUrl, headers=headers)
    
    # Save the response as a JSON file so we can load it into an object
    jsonFile = open(outputFilePath, 'w+')
    jsonFile.write(response.text)
    jsonFile.close()

##################################################################################################################################
# This function fetchs the translation file from the Qualtrics website and saves it as a JSON file
##################################################################################################################################
def FetchSurveyTranslationJSON( surveyID,
                                outputFilePath,
                                langCode = 'FR-CA'):
    # Setting user Parameters   
    apiToken = settings.QUATRICS_API['api_token']
    dataCenter = settings.QUATRICS_API['data_center']
    
    baseUrl = "https://{0}.qualtrics.com/API/v3/surveys/{1}/translations/{2}".format(dataCenter, surveyID, langCode)
    headers = {"x-api-token": apiToken,}
    
    response = requests.get(baseUrl, headers=headers)

    # Save the response as a JSON file so we can load it into an object
    jsonFile = open(outputFilePath, 'w+')
    jsonFile.write(response.text)
    jsonFile.close() 
     
##################################################################################################################################
# This funciton downloads the specific survey response data from Qualtrics website and saves it as a JSON file
##################################################################################################################################          
def FetchSurveyReponsesJSON(surveyID,
                            outputFilePath,
                            responseJSONFileName):
   
    # Setting user Parameters
    api_token = settings.QUATRICS_API['api_token']
    data_center = settings.QUATRICS_API['data_center'] 

    file_format = "json"
       
    # Setting static parameters
    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    # Step 1: Creating Data Export
    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '","surveyId":"' + surveyID + '"}' 
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    progress_id = download_request_response.json()["result"]["id"]

    # Step 2: Checking on Data Export Progress and waiting until export is ready
    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)
    request_download = requests.get(request_download_url, headers=headers)
       
    # Step 4: Unzipping the file
    zipFile = zipfile.ZipFile(io.BytesIO(request_download.content))
    zipFile.extractall(outputFilePath)
    
    # Change the file name
    filename = ''
    if len(zipFile.namelist()) == 1:
        filename = '/'+zipFile.namelist()[0]
    
    oldName = outputFilePath + filename
     
    os.rename(oldName, responseJSONFileName)    

##################################################################################################################################
# Main function 
##################################################################################################################################  

def FetchDataMain(aSurvey):

    # Define the file paths for all the files which will be download from the Qualtics website
    englishJSONFilePath = os.path.join( settings.BASE_DIR, 
                                        settings.DATA_DIR_PATH, 
                                        aSurvey.qualtricsSurveyID, 
                                        settings.QUESTION_ENGLISH_JSON_FILENAME)
    frenchJSONFilePath = os.path.join(  settings.BASE_DIR, 
                                        settings.DATA_DIR_PATH, 
                                        aSurvey.qualtricsSurveyID, 
                                        settings.QUESTION_FRENCH_JSON_FILENAME)
    responseJSONFilePath = os.path.join(settings.BASE_DIR, 
                                        settings.DATA_DIR_PATH, 
                                        aSurvey.qualtricsSurveyID, 
                                        settings.RESPONSE_DATA_JSON_FILENAME)
    
    # ToDo: This could be defined before the other paths and than used in their construction
    outputPath =  os.path.join(settings.BASE_DIR, 
                               settings.DATA_DIR_PATH,
                               aSurvey.qualtricsSurveyID)

    print(outputPath)
    # create the output folder if it does not exist already
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # # Fetch the survey question data from the Qualtric website
    print('FetchSurveyQuestionsJSON')
    FetchSurveyQuestionsJSON(   aSurvey.qualtricsSurveyID,
                                englishJSONFilePath)
    
    print('FetchSurveyTranslationSON')
    FetchSurveyTranslationJSON( aSurvey.qualtricsSurveyID,
                                frenchJSONFilePath)

    # Fetch the survey response data from the Qualtric website
    print('FetchSurveyReponsesJSON')
    FetchSurveyReponsesJSON(aSurvey.qualtricsSurveyID,
                            outputPath,
                            responseJSONFilePath)