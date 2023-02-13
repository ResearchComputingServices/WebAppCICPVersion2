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
       
    title = GetGraphicTitle(question, isEnglish)
    
    # Generate the responseDict (choiceID:average as the key:value pair)
    # initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)
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
        
        if response.answerValue != None:
            value = int(response.answerValue)
            responseDict[key] += value
            counter[key] += 1
            totalResponses +=1
 
    # calculate the average        
    for key in responseDict.keys():
        if float(counter[key]) > 0:
            responseDict[key] = float(responseDict[key]) / float(counter[key]) 
            
    return CreateVerticalBarChart(  responseDict, 
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

def CreateVerticalBarChart( responseDict,
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

    # Annotation Text
    annotationText = ''
    if isEnglish:
        annotationText = '# of Responses: '+str(numberOfResponses)
    else:
        annotationText = '# de Réponses: '+str(numberOfResponses)

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
                    orientation='h',
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX)
    
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