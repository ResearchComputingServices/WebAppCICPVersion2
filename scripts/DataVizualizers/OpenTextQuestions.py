import os
import uuid

import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import colors
import matplotlib.image as image

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################

def VisualizeOpenTextQuestion(  question, 
                                userResponses,
                                numOfRespondents,
                                isEnglish=True,
                                saveToDirPath = TMP_FIGURE_FOLDER_PATH):
    
    title = GetGraphicTitle(question, isEnglish)
       
    # Get text for wordcloud generation 
    allResponseText = ''
    for response in userResponses:
        # responseText = ''
        # if isEnglish:
        #     responseText = response.answerTextEnglish
        # else:
        #     responseText = response.answerTextFrench     
        responseText = response.answerTextOriginal

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
                    saveToDirPath = TMP_FIGURE_FOLDER_PATH):   
   
    # define colours to use
    red = np.array([233/256, 28/256, 36/256, 1])
    cmap = colors.ListedColormap([red, 'black'])
       
    # create the word cloud object
    wc = WordCloud(font_path=FONT_LOCATION,
                   width=FIGURE_WIDTH_PX,
                   height=FIGURE_HEIGHT_PX,
                   background_color='white',
                   colormap=cmap)
        
    reportDate = saveToDirPath.split("/")[-1] 
    
    # Prepare the text for creating a word cloud by translating it and removing stop words 
    destCode = 'fr'
    if isEnglish:
        destCode = 'en'

    if len(wordCloudText) == 0:
        wordCloudText = 'ERRROR1'
    
    wordCloudText = GetTextForWordCloud(wordCloudText, destCode)

    if len(wordCloudText) == 0:
        wordCloudText = 'ERRROR2'

    # produce the actual wordcloud
    wc.generate(wordCloudText)
    
    fig = plt.figure(figsize=(8,8))
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
    ax1.set_title(title+'\n',loc='center',wrap=True)
    ax1.imshow(wc)
    plt.axis('off')
            
    # Get the watermark image and add it to the figure
    waterMarkImg = image.imread(WATERMARK_IMAGE_FILE_PATH)
    ax2 = fig.add_axes([0.,-0.1,0.2,0.2], anchor='NE', zorder=1)
    ax2.imshow(waterMarkImg)
    ax2.axis('off')

    ax3 = fig.add_axes([0.75,0.01,0.25,0.1], anchor='NE', zorder=1)
    reportDate = saveToDirPath.split("/")[-1] 
    aText = GetAnnotation(numberOfResponses, reportDate, isEnglish)
    annotateText = aText[0]+'\n'+aText[1]
    ax3.annotate(annotateText, xy=(1.,0.),xycoords='axes fraction',horizontalalignment='right')
    ax3.axis('off')

    # save the wordcloud to a file
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format=GRAPHIC_FILE_TYPE)
    plt.close(fig)   
    
    return figureFilePath
    