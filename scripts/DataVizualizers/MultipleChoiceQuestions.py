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
                                    numOfRespondents,
                                    isEnglish = True,
                                    saveToDirPath = TMP_FIGURE_FOLDER_PATH):    
    title = GetGraphicTitle(question, isEnglish)
        
    # Generate the responseDict (choiceID:average as the key:value pair) initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)
    responseDict = {}
    totalResponses = numOfRespondents
    totalResponses1 = 0

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
            totalResponses1 +=1
    
    for key in responseDict.keys():
        if float(totalResponses1) > 0:
            responseDict[key] = float(responseDict[key]) / float(totalResponses1)   
       
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
            names.append(WrapText(maxKey,20))
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

    fig = plt.figure(figsize=(12,12))
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
    ax1.set_title(graphicTitle+'\n',loc='center',wrap=True)


    #ax1.pie(values,
        #labels=names,
        #autopct='%1.1f%%',
        #pctdistance=0.8,
        #colors=cmap, 
        #startangle=90,
        #counterclock=False)

    #Added to modify pie chart - Rohan
    perc = [str(round(e / s * 100., 2)) + '%' for s in (sum(values),) for e in values]
    
    wedges, texts = ax1.pie(values,
                            #labels=names,
                            wedgeprops=dict(width=0.5),
                            #autopct='%1.1f%%',
                            pctdistance=0.8,
                            colors=cmap, 
                            startangle=-40,
                            counterclock=False)

    #wedges, texts = ax.pie(data, wedgeprops=dict(width=0.5), startangle=-40, radius = 0.8,colors = cmap)
    kw = dict(arrowprops=dict(arrowstyle="-"),zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1) / 2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        yc = np.arcsin(y) / (np.pi / 2)
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f'angle,angleA=0,angleB={ang}'
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        #ax1.annotate(names[i] + ' ' + str(values[i]), xy = (0.5 * x, 0.5 * y), xytext = ((1.0 + (i % 2) * 0.4) * np.sign(x), 1.4 * yc),
                    #horizontalalignment = horizontalalignment, fontsize = 'x-small', **kw)
        ax1.annotate(str(perc[i]), xy = (0.8 * x, 0.8 * y), xytext = ((1.0 + (i % 2) * 0.4) * np.sign(x), 1.4 * yc),
                    horizontalalignment = horizontalalignment, fontsize = 'x-small', **kw)

    plt.subplots_adjust(right=0.8)
    plt.legend(names, bbox_to_anchor=(1.03 ,1.), loc="upper left")
    
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