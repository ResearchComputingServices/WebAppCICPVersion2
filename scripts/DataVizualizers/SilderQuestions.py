import pandas as pd
import plotly.express as px


from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################

def VisualizeSliderQuestion(question, 
                            userResponses,
                            isEnglish = True,
                            saveToDirPath = FIGURE_FOLDER_PATH): 
    
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
                                        saveToDirPath = FIGURE_FOLDER_PATH):    
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
    if maxValue <= 10:
        maxValue = 10
    elif maxValue <= 100:
        maxValue = 100
    
    if minValue >= 0:
        minValue = 0
    elif minValue >= -10:
        minValue = -10
    elif minValue >= -100:
        minValue = -100
    
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
    
    responseDataFrame['bin'] = bin
    responseDataFrame['value'] = value
      
    # print(valueDict)
    # print('min:', minValue)
    # print('max:', maxValue)
    # print(responseDataFrame)
    # input()
    
    return CreateVerticleBarChart(  responseDataFrame=responseDataFrame,
                                    graphicTitle=title,
                                    numberOfResponses=numberOfResponses,
                                    isEnglish = isEnglish,
                                    saveToDirPath = saveToDirPath)
##################################################################################################################################
#
##################################################################################################################################

def CreateVerticleBarChart( responseDataFrame,
                            graphicTitle,
                            numberOfResponses,
                            isEnglish = True,
                            saveToDirPath = FIGURE_FOLDER_PATH):
    # create the actual plot object
    fig = px.bar(   responseDataFrame,
                    x='bin', 
                    y='value',
                    title=graphicTitle,
                    # color="names",
                    text_auto='.2s',
                    color_discrete_sequence=['rgb(233,28,36)'],
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)      
    
    # update the layout of the figure
    fig.update_layout(  font_family='Helvetica Now', 
                        font_color="black",
                        plot_bgcolor='rgb(232,232,232)',
                        title_font={'size': 20},
                        showlegend=False)
                            
    AddAnnotation(fig, numberOfResponses, isEnglish)

    return SaveFigure(fig, saveToDirPath)

 
##################################################################################################################################
#
##################################################################################################################################
def VisualizeMultiChoiceSliderQuestion( title, 
                                        choiceQuerySet,
                                        userResponses,
                                        isEnglish = True,
                                        saveToDirPath = FIGURE_FOLDER_PATH):  
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

def DetermineBarColours(values):

    colourMap = []
        
    carletonRed = 'rgb(233,28,36)'
    black = 'rgb(0,0,0)'
      
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
#
##################################################################################################################################

def CreateHorizontalBarChart(   responseDict,
                                graphicTitle,
                                numberOfResponses,
                                isEnglish = True,
                                saveToDirPath = FIGURE_FOLDER_PATH):
   
    # Now that we have the extracted data we can create the graphic. 
    # the "values" and "names" are passed to the graphic object as lists    
    values = []
    names = []

    # sort the incoming data and store it in lists which can be passed to ploly 
    responseDict_sorted = sorted(responseDict.items(), key=lambda x:x[1])
    responseDict_sorted.reverse()
    for item in responseDict_sorted:
        names.append(WrapText(item[0], 30))
        values.append(float(item[1]))

    colourMap = DetermineBarColours(values)
     
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

    # x-axis title
    xAxisTitle = ''
    if isEnglish:
        xAxisTitle = 'Mean of the Responses '
    else:
        xAxisTitle = 'Moyenne des réponses'

    # Get the title
    graphTitle = WrapText(graphicTitle)
      
    # Start creating the graphic    
    df = pd.DataFrame(columns=['names','values'])
    df['names'] = names
    df['values'] = values
    
    # create the actual plot object
    fig = px.bar(   df,
                    y='names', 
                    x='values',
                    title=graphTitle,
                    color="names",
                    text_auto='.2s',
                    color_discrete_sequence=colourMap,
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX,
                    orientation='h')
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)      
    
    # update the layout of the figure
    fig.update_layout(  font_family='Helvetica Now', 
                        font_color="black",
                        plot_bgcolor='rgb(232,232,232)',
                        title_font={'size': 20},
                        showlegend=False,
                        xaxis_range=[xMin,xMax])
        
    fig.update_xaxes(   visible=True, 
                        showline=True,
                        gridcolor='rgb(152,152,152)',
                        showticklabels=True, 
                        tickangle = -45, 
                        automargin =  True, 
                        title=xAxisTitle,
                        tickfont={'size': 15},
                        tickvals=tickValues,
                        ticktext=tickLabels)
    
    fig.update_yaxes(   visible=True,
                        showticklabels=True,
                        tickangle = 0,
                        automargin =  True,
                        title='',
                        tickfont={'size': 15})                       

    AddAnnotation(fig, numberOfResponses, isEnglish)

    return SaveFigure(fig, saveToDirPath)