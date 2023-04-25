import pandas as pd
import plotly.express as px

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from textwrap import fill

##################################################################################################################################
#
##################################################################################################################################
def VisualizeRankOrderQuestion( question, 
                                userResponses,
                                isEnglish = True,
                                saveToDirPath = TMP_FIGURE_FOLDER_PATH): 
    
    title = GetGraphicTitle(question, isEnglish)
    
    # Generate the responseDict (choiceID:average as the key:value pair) initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)
        
    totalResponses = len(userResponses)
    
    # Create the response dictionary
    responseDict= {}
    
    for response in userResponses:
        choice = choiceQuerySet.filter(id=response.choiceID.id).first()  
        
        choiceText = ''
        if isEnglish:
            choiceText = choice.choiceTextEnglish
        else:
            choiceText = choice.choiceTextFrench
        
        if choiceText in responseDict.keys():
            responseDict[choiceText].append(response.answerValue)
        else:
            responseDict[choiceText] = []
            
    finalResponseDicts = {}
    
    for key in responseDict:
        listOfRanks = responseDict[key]
        
        rankCount = {}
        
        for rank in listOfRanks:
            if rank == '1':
                if '1st' in rankCount.keys():
                    rankCount['1st'] += 1
                else:
                    rankCount['1st'] = 0
            elif rank == '2':
                if '2nd' in rankCount.keys():
                    rankCount['2nd'] += 1
                else:
                    rankCount['2nd'] = 0
            elif rank == '3':
                if '3rd' in rankCount.keys():
                    rankCount['3rd'] += 1
                else:
                    rankCount['3rd'] = 0
            else:
                if '4th +' in rankCount.keys():
                    rankCount['4th +'] += 1
                else:
                    rankCount['4th +'] = 0
    
        finalResponseDicts[key] = rankCount
    
    # send everything to the figure creator
    return CreateStackedBarChart(   finalResponseDicts, 
                                    title,
                                    totalResponses,
                                    isEnglish,
                                    saveToDirPath)
                
    
##################################################################################################################################
#
##################################################################################################################################

def CreateStackedBarChart(  responseDict,
                            graphicTitle,
                            numberOfResponses,
                            isEnglish = True,
                            saveToDirPath = TMP_FIGURE_FOLDER_PATH):
    
    #####################################################################
    # ToDo: move this code block to a separate function
    # Rearrange the incoming data into a format we can plot   
    
    # get col
    columns = ['subQ']
    subQs = []
    for subQ in responseDict.keys():
        
        if subQ not in subQs:
            subQs.append(subQ)
        
        for response in responseDict[subQ].keys():
            if response not in columns:
                columns.append(response)
    
    # create data frame with correct rows
    df = pd.DataFrame(columns=columns)
    
    # populate elements
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            value = responseDict[subQ][response]
            df.at[subQ, response] = value
            df.at[subQ, 'subQ'] = 0.
    
    # normalize rows (magic, I dont know how this works)
    df = df.div(df.sum(axis=1), axis=0) 
    df = df.multiply(100)
    
    # change subQ to have the correct names
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            df.at[subQ, 'subQ'] = fill(subQ,15)
    #####################################################################3   
   
    # define colours to use
    colourMap = [(0/255,0/255,0/255),
                (233/255,28/255,36/255),
                (45/255,45/255,45/255),
                (242/255,121/255,126/255),
                (151/255,151/255,151/255),
                (145/255,14/255,19/255),
                (51/255,51/255,51/255),
                (185/255,44/255,49/255)]

    cmap = LinearSegmentedColormap.from_list('my_colours', colourMap)
        
    # Create the figure which plots the bar chart
    # creating the bar plot
    fig = plt.figure(figsize=(8,8))
    plt.subplots_adjust(left=0.22)
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
   
    # plot data in stack manner of bar type
    df.plot(x='subQ', 
            kind='barh', 
            stacked=True,
            ax=ax1,
            colormap=cmap)
    
    ax1.set_title(graphicTitle,wrap=True)
    ax1.set_ylabel('')
    ax1.set_xticks([0,25,50,75,100])
    
    if isEnglish:
        ax1.set_xlabel('% of Responses')
    else:
        ax1.set_xlabel('% de réponses')
       
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

    # plt.show() 

    # save the wordcloud to a file
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format=GRAPHIC_FILE_TYPE)
    plt.close(fig)   
    
    return figureFilePath
