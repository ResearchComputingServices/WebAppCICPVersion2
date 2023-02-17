import pandas as pd
import plotly.express as px

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *

##################################################################################################################################
#
##################################################################################################################################
def VisualizeRankOrderQuestion( question, 
                                userResponses,
                                isEnglish = True,
                                saveToDirPath = FIGURE_FOLDER_PATH): 
    
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
                                    saveToDirPath)
                
    
##################################################################################################################################
#
##################################################################################################################################

def CreateStackedBarChart(  responseDict,
                            graphicTitle,
                            numberOfResponses,
                            isEnglish = True,
                            saveToDirPath = FIGURE_FOLDER_PATH):
    
    df = pd.DataFrame(columns=['subQ','response','value'])
    
    iRow = 0
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            value = responseDict[subQ][response]
            
            df.loc[iRow] = [subQ,response, value]
            
            iRow += 1
    
    colourMap = ['rgb(0,0,0)',
                'rgb(233,28,36)',
                'rgb(200,200,200)',
                'rgb(242,121,126)',
                'rgb(151,151,151)',
                'rgb(145,14,19)',
                'rgb(51,51,51)',
                'rgb(185,44,49)']

    # Get the title
    graphicTitle = WrapText(graphicTitle)       
     
    # create the actual plot object
    fig = px.bar(   df, 
                    color="response", 
                    y="subQ", 
                    x="value", 
                    title=graphicTitle,
                    color_discrete_sequence=colourMap,
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX,
                    orientation='h')
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)      
    
    # update the layout of the figure
    fig.update_layout(  font_family='Helvetica Now', 
                        font_color="black",
                        plot_bgcolor='rgb(232,232,232)',
                        title_font={'size': 20})
        
    AddAnnotation(fig, numberOfResponses, isEnglish)

    return SaveFigure(fig,saveToDirPath)
