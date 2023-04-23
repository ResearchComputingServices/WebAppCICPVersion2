import plotly.express as px

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

    graphTitle = WrapText(graphicTitle)
        
    # Now that we have the extracted data can create the graphic. 
    # the "values" and "names" are passed to the graphic object as lists
    values = []
    names = []

    for key in responseDict.keys():
        names.append(WrapText(key, 30))
        values.append(responseDict[key])
        
    # define colours to use
    cmap = ['rgb(0,0,0)',
            'rgb(233,28,36)',
            'rgb(200,200,200)',
            'rgb(242,121,126)',
            'rgb(151,151,151)',
            'rgb(145,14,19)',
            'rgb(51,51,51)',
            'rgb(185,44,49)']

    fig = px.pie(   values=values, 
                    names=names,
                    title=graphTitle,
                    hole=PIE_CHART_HOLE_RADIUS,
                    template='presentation',
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX,
                    color_discrete_sequence=cmap)

    fig.update_layout(font_family='Helvetica Now', 
                      font_color="black",
                      title_font={'size': 20},
                      legend_font={'size': 15},
                      legend={'traceorder':'reversed', "yanchor":"top","y":0.50,"xanchor":"right","x":1.75},
                       margin=dict(l=100, r=300, t=150, b=320),)
    #x axis
    fig.update_xaxes(visible=False)

    #y axis    
    fig.update_yaxes(visible=False)

    reportDate =  saveToDirPath.split("/")[-1]                 

    AddAnnotation(fig, numberOfResponses, reportDate, isEnglish)
      
    return SaveFigurePie(fig,saveToDirPath)