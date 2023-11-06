from scripts.Utils import *
from InteractiveDB.models import SurveyTable
from datetime import date
import requests
from icecream import ic

def AddSurvey(id,date,theme,subthemeEnglish,subthemeFrench,surveyWeek):
    survey = SurveyTable()
    survey.qualtricsSurveyID = id
    survey.releaseDate = date
    survey.surveyTheme = theme
    survey.surveysubThemeEnglish = subthemeEnglish
    survey.surveysubThemeFrench = subthemeFrench
    survey.surveyWeek = surveyWeek

    survey.save()

# API 1 - GetAllSurveys API

def getAllSurveys():

    url = "https://ca1.qualtrics.com/API/v3/surveys"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'X-API-TOKEN': 'sWArU3xit6H1SbAYGzC1MPdornLOKQJLAWKIfzmU'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    responseBody = response.json()
    surveys = responseBody['result']['elements']

    # Filter surveys with name containing "Yr1 Wk"
    filteredSurveys = list(filter(
        lambda survey: "Yr1 Wk" in survey['name'] and len(survey['name']) <= 8, surveys))
    for survey in filteredSurveys:
        if len(survey['name'].split(" ")[1]) == 3:
            survey['name'] = survey['name'].replace("Wk", "Wk0")

    filteredSurveys.sort(key=lambda survey: survey['name'])
    surveyIds = []

    for survey in filteredSurveys:
        surveyIds.append(survey['id'])
        # Only get the surveyIds that are published by using the status True for the most recently published survey.
        # Once you see a True it means that is the latest survey and so we stop there.
        if survey['isActive'] == True:
            break
    return surveyIds

# API 2 - Get Survey Meta Data

def performRequest(latestSurveyId,apiName):

    headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": "sWArU3xit6H1SbAYGzC1MPdornLOKQJLAWKIfzmU"
    }

    url = "https://yul1.qualtrics.com/API/v3/survey-definitions/"+latestSurveyId+apiName

    return requests.request("GET", url, headers=headers).json()

# The Survey Description is in the format (Theme;subthemeEnglish;subthemeFrench)
# This function extracts each value
def splitSurveyDescription(surveyDescription,name):

    if surveyDescription == "null":
        return "SurveyDescription is null"

    if name == "theme":
        return surveyDescription.split(";")[0]
    
    if name == "subthemeEnglish":
        return surveyDescription.split(";")[1]

    if name == "subthemeFrench":
        return surveyDescription.split(";")[2]

# The surveyName needs to be formatted to match the database setup and sort them in the right order.
def formatSurveyWeek(surveyName):
    parts = surveyName.split()

    if len(parts) == 2 and parts[0].startswith("Yr") and parts[1].startswith("Wk"):
        year = parts[0][2:]
        week = parts[1][2:].zfill(2)
        return f"Y{year}W{week}"
##################################################################################################################################
# Main function 
# - this function will be called every Wednesday by the cronJob
# - it will use the GetSurveys API and fetch the surveys that are published till now
#   and stops at the last active survey which is our latest survey.
# - It then uses the GetSurveyMetaData API to get the status of the latest survey to make sure it is active
# - If the status is active then we use this surveyId to get the SurveyDescription which has the theme,subThemeEnglish,subthemeFrench, and the SurveyName which are then passed to different functions for preprocessing.
# - Finally all the parameters are passed to the AddSurvey to create the survey in the backend database. 
################################################################################################################################## 
def run(*args):
    

    # # Fetches the surveys already in the database
    # surveyQuerySet = SurveyTable.objects.all()

    # List of surveys from Qualtrics tool
    surveyIDs = getAllSurveys()

    # The last active survey is the last ID in the list
    latestSurveyId = surveyIDs[-1]


    # This request is used to get the status of the survey.The status should be active to proceed further.
    metaDataResponse  = performRequest(latestSurveyId,apiName="/metadata")
    ic(metaDataResponse)
    
    if metaDataResponse["result"]["SurveyStatus"] == "Active":


        # This request fetches the required fields from the options API.
        optionsResponse  = performRequest(latestSurveyId,apiName="/options")
        ic(optionsResponse)

        surveyMetaDescription = optionsResponse["result"]["SurveyMetaDescription"]
        surveyName = metaDataResponse["result"]["SurveyName"]

        # The ID remains the latestsurveyID.
        # The cronjob runs every wednesday because the survey is usualy released on that day of the week.

        AddSurvey(id=latestSurveyId,
                  date=date.today(),
                  theme=splitSurveyDescription(surveyMetaDescription,"theme"),
                  subthemeEnglish=splitSurveyDescription(surveyMetaDescription,"subthemeEnglish"),
                  subthemeFrench=splitSurveyDescription(surveyMetaDescription,"subthemeFrench"),
                  surveyWeek=formatSurveyWeek(surveyName)
        )
    else:
        print("Survey is not yet active")
