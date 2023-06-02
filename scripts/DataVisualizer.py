import os

from scripts.Utils import *
from scripts.DataVizualizers.SilderQuestions import VisualizeSliderQuestion
from scripts.DataVizualizers.MultipleChoiceQuestions import VisualizeMultipleChoiceQuestion   
from scripts.DataVizualizers.OpenTextQuestions import VisualizeOpenTextQuestion                        
from scripts.DataVizualizers.MatrixQuestions import VisualizeMatrixQuestion
from scripts.DataVizualizers.RankOrderQuestions import VisualizeRankOrderQuestion                        
from scripts.DataVizualizers.TextGraphicQuestions import VisualizeTextGraphicQuestion

import time

# This dictionary connects question type flags to the visualizer that creates the graphic for them
questionHandleDict ={   SLIDER_QUESTION : VisualizeSliderQuestion,
                        MULTIPLE_CHOICE_QUESTION : VisualizeMultipleChoiceQuestion,
                        OPEN_TEXT_QUESTION : VisualizeOpenTextQuestion,
                        MATRIX_QUESTION : VisualizeMatrixQuestion,
                        RANK_ORDER_QUESTION : VisualizeRankOrderQuestion,
                        TEXT_GRAPHIC_QUESTION : VisualizeTextGraphicQuestion}

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
# This function is the main entry point into the DataVisualizer. It will be called by the Controller to generate the images
# which it will then send to the Front End. It will return a list of file paths to the location of the generated files
##################################################################################################################################
def DataVisualizerMain(responseDict,
                       isEnglish = True,
                       saveToDirPath = TMP_FIGURE_FOLDER_PATH):

    # make sure the tmp folder for storing the generated images exists
    isExist = os.path.exists(saveToDirPath)
    if not isExist:
        os.makedirs(saveToDirPath)
    
    imageFilePathList = []
    
    for question in responseDict.keys():
       
        if question.questionTheme in QUESTION_THEME_SKIP_LIST:
            continue
            
        if question.questionType not in questionHandleDict.keys():
            print('[ERROR]: Unknown question type: ', question.questionType)
        else:                                              
            s = time.time()
            
            lstOfRespondents = {}
            for r in responseDict[question]:
                lstOfRespondents[r.userID.id] = 1
            numOfRespondents = len(list(lstOfRespondents.keys()))
            print(numOfRespondents)

            imageFilePath = questionHandleDict[question.questionType](  question = question,
                                                                        userResponses = responseDict[question],
                                                                        numOfRespondents = numOfRespondents, 
                                                                        isEnglish= isEnglish,
                                                                        saveToDirPath = saveToDirPath) 
            e = time.time()
            print(question.questionType,':', e - s)
            imageFilePathList.append(imageFilePath)
               
    return imageFilePathList

##################################################################################################################################
# This function can be used for testing the data visualizers and the FrontEndQuery object
##################################################################################################################################

def run(*arg):
    
    # make sure the tmp folder for storing the generated images exists
    isExist = os.path.exists(TMP_FIGURE_FOLDER_PATH)
    if not isExist:
        os.makedirs(TMP_FIGURE_FOLDER_PATH)
    
    # create a front end query to get some data from the DB
    aQuery = FrontEndQuery()   
    aQuery.date = '2023-01-01'
    #aQuery.locations = 'AB'

    #userResponseQuerySet = GetUserResponseQuerySet(aQuery)
    #listOfFilePaths = DataVisualizerMain(userResponseQuerySet)
    
    # for fp in listOfFilePaths:
    #     print(fp)
    
    
        
  
