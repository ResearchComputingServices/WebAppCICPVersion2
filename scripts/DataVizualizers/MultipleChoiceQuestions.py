import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import colors
import matplotlib.image as image
from textwrap import fill

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################

def VisualizeMultipleChoiceQuestion(question, 
                                    userResponses,
                                    isEnglish = True,
                                    saveToDirPath = TMP_FIGURE_FOLDER_PATH):    
    title = GetGraphicTitle(question, isEnglish)
        
    # Generate the responseDict (choiceID:average as the key:value pair) initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)
    responseDict = {}
    totalResponses = 0   

    for choice in choiceQuerySet:
        key = ''
        if isEnglish:
            key = choice.choiceTextEnglish
        else:
            key = choice.choiceTextFrench
            
        responseDict[key] = 0
    
    # fill the responseDict with the values in userResponses
    for response in userResponses:
    
        # if there is no choiceID associated with this response it means
        # it is a free text response and will be handled seperately
        if response.choiceID == None:
            continue
    
        key = ''
        if isEnglish:
            key = choiceQuerySet.filter(id=response.choiceID.id).first().choiceTextEnglish
        else:
            key = choiceQuerySet.filter(id=response.choiceID.id).first().choiceTextFrench
        
        if response.answerValue != None and str(response.answerValue).isnumeric():
            value = int(response.answerValue)
            responseDict[key] += value
            totalResponses +=1
    
    for key in responseDict.keys():
        if float(totalResponses) > 0:
            responseDict[key] = float(responseDict[key]) / float(totalResponses)   
       
    return CreatePieChart(  responseDict, 
                            title, 
                            totalResponses,
                            isEnglish,
                            saveToDirPath)

##################################################################################################################################
#
##################################################################################################################################

def CreatePieChart( responseDict,
                    graphicTitle,
                    numberOfResponses,
                    isEnglish = True,
                    saveToDirPath = TMP_FIGURE_FOLDER_PATH):
            
    # Now that we have the extracted data can create the graphic. 
    # the "values" and "names" are passed to the graphic object as lists
    values = []
    names = []

    while len(responseDict.keys()) > 0:
        maxKey = ''
        maxValue = -1.

        # find the max key and value
        for key in responseDict.keys():
            
            currentValue = responseDict[key]
            if currentValue > maxValue:
                maxValue = currentValue
                maxKey = key
            
        responseDict.pop(maxKey)
            
        # add the max to the list
        if maxValue > 0.:
            names.append(fill(maxKey,20))
            values.append(maxValue)
        
    if len(names) > 7:
        
        otherValue = 0
        for value in values[7:]:
            otherValue += value
        
        names = names[:7]
        values = values[:7]
        
        names.append('other')
        values.append(otherValue)  
        
    # define colours to use
    cmap = [(233/255,28/255,36/255),
            (45/255,45/255,45/255),
            (242/255,121/255,126/255),
            (151/255,151/255,151/255),
            (145/255,14/255,19/255),
            (51/255,51/255,51/255),
            (185/255,44/255,49/255),
            (200/255,200/255,200/255)]

    # Create the figure which plots the pie chart
    plt.title(graphicTitle+'\n',loc='center',wrap=True)
    plt.axis('off')
    
    plt.pie(values,
            #labels=names,
            autopct='%1.1f%%',
            pctdistance=0.8,
            colors=cmap, 
            startangle=90,
            counterclock=False)
    
    # Add the legend
    plt.legend(names, bbox_to_anchor=(0.9 ,1.), loc="upper left")
    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)  
    
    # draw circle
    centre_circle = plt.Circle((0, 0), PIE_CHART_HOLE_RADIUS, fc='white')
    fig = plt.gcf()
    fig.set_size_inches(w=8.,h=8)
    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)
    
    # Get the annotation text and add it to the figure
    reportDate = saveToDirPath.split("/")[-1] 
    aText = GetAnnotation(numberOfResponses, reportDate, isEnglish)
    plt.figtext(x=1., y=0., s=aText[0]+'\n'+aText[1],horizontalalignment='right')
    
    # Get the watermark image and add it to the figure
    waterMarkImg = image.imread(WATERMARK_IMAGE_FILE_PATH)
    newax = fig.add_axes([0.,-0.1,0.2,0.2], anchor='NE', zorder=1)
    newax.imshow(waterMarkImg)
    newax.axis('off')

    # save the wordcloud to a file
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format=GRAPHIC_FILE_TYPE)
    plt.close(fig)
         
    return figureFilePath