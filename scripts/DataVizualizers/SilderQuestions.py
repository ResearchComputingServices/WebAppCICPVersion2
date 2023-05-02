import pandas as pd
import plotly.express as px
import plotly.subplots as sp

import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.image as image
from textwrap import fill

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################

def VisualizeSliderQuestion(question, 
                            userResponses,
                            isEnglish = True,
                            saveToDirPath = TMP_FIGURE_FOLDER_PATH): 
    
    filename = ''
      
    title = GetGraphicTitle(question, isEnglish)
    
    # Generate the responseDict (choiceID:average as the key:value pair)
    # initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)  
   
    if len(choiceQuerySet) == 1:
        filename = VisualizeSingleChoiceSliderQuestion( title=title,
                                                        choiceQuerySet=choiceQuerySet,
                                                        userResponses=userResponses,
                                                        isEnglish=isEnglish,
                                                        saveToDirPath=saveToDirPath)
    else:
        filename = VisualizeMultiChoiceSliderQuestion( title=title,
                                                        choiceQuerySet=choiceQuerySet,
                                                        userResponses=userResponses,
                                                        isEnglish=isEnglish,
                                                        saveToDirPath=saveToDirPath)
    
    return filename

##################################################################################################################################
#
##################################################################################################################################
def VisualizeSingleChoiceSliderQuestion(title, 
                                        choiceQuerySet,
                                        userResponses,
                                        isEnglish = True,
                                        saveToDirPath = TMP_FIGURE_FOLDER_PATH):    
    # Create a histogram of responses
    valueDict = {}
    minValue = A_LARGE_NUMBER
    maxValue = -1*A_LARGE_NUMBER
    numberOfResponses = len(userResponses)
    for response in userResponses:
        
        if response.answerValue == None or not str(response.answerValue).isnumeric():
            continue
        
        value = int(response.answerValue)
        
        # update histo
        if value in valueDict.keys():
            valueDict[value] += 1
        else:
            valueDict[value] = 1
            
        # update bounds
        if value < minValue:
            minValue = value
        if value > maxValue:
            maxValue = value
            
    # pad the min and max
    maxValue = roundup(maxValue)
    
    if minValue >= 0:
        minValue = 0
    else:
        minValue = -1.*roundup(-1.*minValue)
    
    # now pad the valueDict
    for i in range(minValue, maxValue):
        if i not in valueDict.keys():
            valueDict[i] = 0
        
    # Create a dataframe with the extra padding set to zero
    responseDataFrame = pd.DataFrame(columns=['bin','value'])
   
    value = []
    bin = []

    # sort the incoming data and store it in lists which can be passed to ploly 
    valueDict_sorted = sorted(valueDict.items(), key=lambda x:x[0])
    for item in valueDict_sorted:
        bin.append(str(item[0]))
        value.append(int(item[1]))
        
    return CreateVerticleBarChart(  binList = bin,
                                    valueList = value,
                                    graphicTitle=title,
                                    numberOfResponses=numberOfResponses,
                                    xMin = minValue,
                                    xMax = maxValue,
                                    isEnglish = isEnglish,
                                    saveToDirPath = saveToDirPath)
    
    
##################################################################################################################################
#
##################################################################################################################################
def VisualizeMultiChoiceSliderQuestion( title, 
                                        choiceQuerySet,
                                        userResponses,
                                        isEnglish = True,
                                        saveToDirPath = TMP_FIGURE_FOLDER_PATH):  
    responseDict = {}
    counter = {}
    totalResponses = 0  
   
    for choice in choiceQuerySet:
        key = ''
        if isEnglish:
            key = choice.choiceTextEnglish
        else:
            key = choice.choiceTextFrench
            
        responseDict[key] = 0
        counter[key] = 0
    
    # fill the responseDict with the values in userResponses
    for response in userResponses:
        key = ''
        if isEnglish:
            key = choiceQuerySet.filter(id=response.choiceID.id).first().choiceTextEnglish
        else:
            key = choiceQuerySet.filter(id=response.choiceID.id).first().choiceTextFrench
        
        if response.answerValue != None and str(response.answerValue).isnumeric():
            value = int(response.answerValue)
            responseDict[key] += value
            counter[key] += 1
            totalResponses +=1
 
    # calculate the average        
    for key in responseDict.keys():
        if float(counter[key]) > 0:
            responseDict[key] = float(responseDict[key]) / float(counter[key]) 
            
    return CreateHorizontalBarChart(  responseDict, 
                                    title,
                                    totalResponses,  
                                    isEnglish,
                                    saveToDirPath)

##################################################################################################################################
#
##################################################################################################################################    
    
def CreateVerticleBarChart( binList,
                            valueList,
                            graphicTitle,
                            numberOfResponses,
                            xMin,
                            xMax,
                            isEnglish = True,
                            saveToDirPath = TMP_FIGURE_FOLDER_PATH):
    
    
    # Create the figure which plots the bar chart
    # creating the bar plot
    fig = plt.figure(figsize=(8,8))
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
    ax1.set_title(graphicTitle+'\n',loc='center',wrap=True)
    ax1.bar( binList, 
            valueList, 
            color = (233/255,28/255,36/255))   
    
    ax1.set_ylabel('Frequency')
    ax1.set_xlim(xMin,xMax)
        
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

##################################################################################################################################
#
##################################################################################################################################
 
def DetermineBarColours(values):

    colourMap = []
        
    carletonRed = (233/255,28/255,36/255)
    black = (0,0,0)
      
    # first check if all values have the same sign
    allPositive = True
    allNegative = True
    for val in values:
        if val < 0:
            allPositive = False
        if val > 0:
            allNegative = False
    
    # now based on the signs add the colours in to a list
    if allPositive or allNegative:
        for val in values:
            colourMap.append(carletonRed)
    else:
        for val in values:
            if val < 0:
                colourMap.append(carletonRed)
            else:
                colourMap.append(black)
    
    return colourMap

##################################################################################################################################

def CreateHorizontalBarChart(   responseDict,
                                graphicTitle,
                                numberOfResponses,
                                isEnglish = True,
                                saveToDirPath = TMP_FIGURE_FOLDER_PATH):
   
    # Now that we have the extracted data we can create the graphic. 
    # the "values" and "names" are passed to the graphic object as lists    
    values = []
    names = []

    # sort the incoming data and store it in lists which can be passed to ploly 
    responseDict_sorted = sorted(responseDict.items(), key=lambda x:x[1])
    responseDict_sorted.reverse()
    for item in responseDict_sorted:
        name = item[0]
        value = item[1]
                
        names.append(WrapText(name,20))
        values.append(round(float(value),1))

    colourMap = DetermineBarColours(values) 
    
    # x-axis title
    xAxisTitle = ''
    if isEnglish:
        xAxisTitle = 'Response Mean'
    else:
        xAxisTitle = 'Moyenne des réponses'
    
    # Determine X-axis labels and range
    tickValues = []
    tickLabels = []
    tickValues, tickLabels = CreateLabels(graphicTitle)    
   
    xMin = 0
    xMax = 0
    if len(tickValues) >= 2:
        xMin = min(tickValues)
        xMax = max(tickValues)
    else:
        xMin = min(values)
        xMax = max(values)
        
        if xMin > 0:
            xMin = 0
        if xMax < 0:
            xMax = 0
        
    # Create the figure which plots the bar chart
    # creating the bar plot
    fig = plt.figure(figsize=(8,8))
    plt.subplots_adjust(left=0.22)
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
    ax1.set_title(graphicTitle+'\n',loc='center',wrap=True)
    ax1.barh(   names, 
                values, 
                color = colourMap)   
    ax1.set_xlabel(xAxisTitle)
    ax1.set_xlim(xMin,xMax)
    ax1.set_xticks(tickValues)
    ax1.set_xticklabels(tickLabels)
    ax1.set_ylabel('')
        
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
