from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *
from scripts.DataVizualizers.OpenTextQuestions import CreateWordCloud

##################################################################################################################################
#
##################################################################################################################################
def VisualizeTextGraphicQuestion(   question, 
                                    userResponses,
                                    isEnglish = True,
                                    saveToDirPath = TMP_FIGURE_FOLDER_PATH): 
    print('VisualizeTextGraphicQuestion')
    title = GetGraphicTitle(question, isEnglish)
        
    # Get text for wordcloud generation 
    allResponseText = ''
    for response in userResponses:
        
        responseText = ''
        if isEnglish:
            responseText = response.answerTextEnglish
        else:
            responseText = response.answerTextFrench
        
        if responseText != None and responseText != '' and not responseText.isnumeric() :
            allResponseText += ' ' + responseText

    return CreateWordCloud( wordCloudText = allResponseText,  
                            title = title,
                            numberOfResponses = len(userResponses),
                            isEnglish = isEnglish,
                            saveToDirPath = saveToDirPath)