import os
import uuid

import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import colors

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################

def VisualizeOpenTextQuestion(  question, 
                                userResponses,
                                isEnglish=True,
                                saveToDirPath = FIGURE_FOLDER_PATH):
    
    title = GetGraphicTitle(question, isEnglish)
       
    # Get text for wordcloud generation 
    allResponseText = ''
    for response in userResponses:
        responseText = response.answerText
        if responseText != None and responseText != '':
            allResponseText += ' ' + responseText
    
    return CreateWordCloud( wordCloudText = allResponseText,  
                            title = title,
                            numberOfResponses = len(userResponses),
                            isEnglish = isEnglish,
                            saveToDirPath = saveToDirPath)

##################################################################################################################################
#
##################################################################################################################################

def CreateWordCloud(wordCloudText, 
                    title,
                    numberOfResponses,
                    isEnglish = True,
                    saveToDirPath = FIGURE_FOLDER_PATH):
    
    if len(wordCloudText.strip()) == 0:
        return False

    # define colours to use
    red = np.array([233/256, 28/256, 36/256, 1])
    cmap = colors.ListedColormap([red, 'black'])
       
    # create the word cloud object
    wc = WordCloud(font_path=FONT_LOCATION,
                   width=FIGURE_WIDTH_PX,
                   height=FIGURE_HEIGHT_PX,
                   background_color='white',
                   colormap=cmap)
    
    
    # produce the actual wordcloud
    wc.generate(wordCloudText)
    fig = plt.figure()
    plt.title(title)
    plt.axis('off') 
    plt.imshow(wc)
    
    # save the wordcloud to a file
    filename = str(uuid.uuid4())
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format="png")
    plt.close(fig)
    
    return figureFilePath