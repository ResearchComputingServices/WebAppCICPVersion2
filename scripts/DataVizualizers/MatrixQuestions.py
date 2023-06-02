from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *
from scripts.DataVizualizers.RankOrderQuestions import CreateStackedBarChart

##################################################################################################################################
#
##################################################################################################################################
def GetSubQuestionResponseDict(listOfUserResponses):
    subQResponseDict = {}
    
    for response in listOfUserResponses:
        if response in subQResponseDict.keys():
            subQResponseDict[response] += 1
        else:
            subQResponseDict[response] = 1
    
    return subQResponseDict

##################################################################################################################################
# 
##################################################################################################################################

def VisualizeMatrixQuestion(question, 
                            userResponses,
                            numOfRespondents,
                            isEnglish = True,
                            saveToDirPath = TMP_FIGURE_FOLDER_PATH): 
    
    # only the Parent Matrix question should be included in the list to be visualized
    if question.parentQuestionID != None:
        return
    
    title = GetGraphicTitle(question, isEnglish)
    
    responseDict= {}
            
    # Get all the subquestions
    subQuestionsQuerySet = QuestionTable.objects.filter(parentQuestionID=question)
    
    totalResponses = numOfRespondents
    
    
    for r in userResponses:
        subQ = subQuestionsQuerySet.filter(id=r.questionID.id).first()
        
        if subQ.questionTextEnglish in responseDict.keys():
            choice = ChoiceTable.objects.filter(questionID=subQ.id, recode = r.answerValue).first()
            
            responseDict[subQ.questionTextEnglish].append(choice.choiceTextEnglish)
        else:
            responseDict[subQ.questionTextEnglish] = []
    
    # need to turn the responseDict into a dictionary of dictionarys.
    # first dictionary key value pair is subQustionText:dict_2
    # the next dictionary (dict_2) has key:value pair responseText:count
    finalResponseDicts = {}
    for key in responseDict:
       dict = GetSubQuestionResponseDict(responseDict[key])
       finalResponseDicts[key] = dict

    return CreateStackedBarChart(   finalResponseDicts, 
                                    title,
                                    totalResponses,
                                    isEnglish,
                                    saveToDirPath)