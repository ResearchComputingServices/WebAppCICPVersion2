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
    print("subQResponseDict",subQResponseDict)
    
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

    questionLabel = question.questionLabel
    title = GetGraphicTitle(question, isEnglish)
    
    responseDict= {}
            
    # Get all the subquestions
    subQuestionsQuerySet = QuestionTable.objects.filter(parentQuestionID=question)
    
    totalResponses = numOfRespondents

 
    
    # for r in userResponses:
    #     subQ = subQuestionsQuerySet.filter(id=r.questionID.id).first()
        
    #     if subQ.questionTextEnglish in responseDict.keys():
    #         choice = ChoiceTable.objects.filter(questionID=subQ.id, recode = r.answerValue).first()
            
    #         choiceText = choice.choiceTextEnglish
    #         if not isEnglish:
    #             choiceText = choice.choiceTextFrench

    #         responseDict[subQ.questionTextEnglish].append(choiceText)
            
    #     else:
    #         print("responseDict.keys()",responseDict.keys())
    #         responseDict[subQ.questionTextEnglish] = []

    for r in userResponses:

        subQ = subQuestionsQuerySet.filter(id=r.questionID.id).first()        

        questionText = subQ.questionTextEnglish
        if not isEnglish:
            questionText = subQ.questionTextFrench       

        if questionText in responseDict.keys():

            choice = ChoiceTable.objects.filter(questionID=subQ.id, recode = r.answerValue).first()            

            choiceText = choice.choiceTextEnglish

            if not isEnglish:
                choiceText = choice.choiceTextFrench         

            responseDict[questionText].append(choiceText)

        else:
            responseDict[questionText] = []
            choice = ChoiceTable.objects.filter(questionID=subQ.id, recode = r.answerValue).first() 
            choiceText = choice.choiceTextEnglish

            if not isEnglish:
                choiceText = choice.choiceTextFrench        

            responseDict[questionText].append(choiceText)
    
    # need to turn the responseDict into a dictionary of dictionarys.
    # first dictionary key value pair is subQustionText:dict_2
    # the next dictionary (dict_2) has key:value pair responseText:count
    finalResponseDicts = {}
    for key in responseDict:
       dict = GetSubQuestionResponseDict(responseDict[key])
       finalResponseDicts[key] = dict

    return CreateStackedBarChart(   finalResponseDicts, 
                                    title,
                                    questionLabel,
                                    totalResponses,
                                    isEnglish,
                                    saveToDirPath)