import re
import os
import uuid

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from matplotlib import colors
from wordcloud import WordCloud

from scripts.Utils import *
from scripts.Controller import HandleFrontEndQuery

##################################################################################################################################
def VisualizeOpenTextQuestion(question, userResponses):
    print('VisualizeOpenTextQuestion')    
   
    title = question.questionTextEnglish
    
    filename = str(uuid.uuid4())
    
    # Get text for wordcloud generation 
    allResponseText = ''
    for response in userResponses:
        responseText = response.answerText
        if responseText != None and responseText != '':
            allResponseText += ' ' + responseText
    
    CreateWordCloud(allResponseText, os.path.join(FIGURE_FOLDER_PATH, filename), title)
        
##################################################################################################################################

# def VisualizeOtherTextQuestion( question, figureFilePathBase):
#     # Get text for wordcloud generation 
#     responseText = ''
#     for response in question.freeText:
#         responseText += ' ' + response
    
#     responseTextEnglish = GetText(responseText, 'en')
#     responseTextFrench = GetText(responseText,'fr')
        
#     CreateWordCloud(responseTextEnglish, figureFilePathBase + ENGLISH_FILE_SUFFIX,"Other Responses")
#     CreateWordCloud(responseTextFrench, figureFilePathBase + FRENCH_FILE_SUFFIX,"Autres Réponses") 

##################################################################################################################################

def VisualizeMultipleChoiceQuestion(question, 
                                    userResponses,
                                    isEnglish = True):    
    
    print('VisualizeMultipleChoiceQuestion')
    
    title = ''
    if isEnglish:
        title = question.questionTextEnglish
    else:
        title = question.questionTextFrench
        
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
        
        if response.answerValue != None:
            value = int(response.answerValue)
            responseDict[key] += value
            totalResponses +=1
    

    for key in responseDict.keys():
        if float(totalResponses) > 0:
            responseDict[key] = float(responseDict[key]) / float(totalResponses)   
    
    filename = str(uuid.uuid4()) 
    CreatePieChart(responseDict, 
                   title, 
                   totalResponses,
                   os.path.join(FIGURE_FOLDER_PATH, filename))
    
##################################################################################################################################
#
##################################################################################################################################

def VisualizeSliderQuestion(question, 
                            userResponses,
                            isEnglish = True): 
       
    print('VisualizeSliderQuestion')
    
    title = ''
    if isEnglish:
        title = question.questionTextEnglish
    else:
        title = question.questionTextFrench
    
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
            
    filename = str(uuid.uuid4())
    CreateVerticalBarChart( responseDict, 
                            title,
                            totalResponses,  
                            os.path.join(FIGURE_FOLDER_PATH, filename))
     

##################################################################################################################################
#
##################################################################################################################################

def CreateStackedBarChart( responseDict,
                            graphicTitle,
                            numberOfResponses,
                            figureFilePath):
    print('CreateStackedBarChart')

##################################################################################################################################
#
##################################################################################################################################

def CreatePieChart( responseDict,
                    graphicTitle,
                    numberOfResponses,
                    figureFilePath):

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
        
    fig.add_annotation( text = '# de réponses / of Responses: '+str(numberOfResponses), 
                        showarrow=False,
                        x = -0.05,
                        y = -0.1)

    fig.update_layout(font_family='Helvetica Now', 
                      font_color="black",
                      title_font={'size': 20},
                      legend_font={'size': 15},
                      legend={'traceorder':'reversed', "yanchor":"bottom","y":-0.6,"xanchor":"center","x":0.3})
    
    fig.write_image(figureFilePath,format='png',engine='kaleido')
    
##################################################################################################################################
#
##################################################################################################################################

def CreateWordCloud(wordCloudText, figureFilePath, title):
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
    plt.savefig(figureFilePath, format="png")
    plt.close(fig)
    
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
                            figureFilePath,
                            isEnglish = True):
   
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
        annotationText = '# of Responses: '
    else:
        annotationText = '# de Réponses: '

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

    fig.add_annotation( text = annotationText +str(numberOfResponses), 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = 1.,
                        y = 1.1)

    fig.write_image(figureFilePath,format='png',engine='kaleido')
    
##################################################################################################################################
# def DataVizMain(report):
    
#     questionHandleDict ={   'Slider':VisualizeSliderQuestion,
#                             'MC':VisualizeMultipleChoiceQuestion,
#                             'TE':VisualizeOpenTextQuestion}
        
#     extractSurveyDataFilePath = os.path.join(settings.BASE_DIR, dataDirPath, extractSurveyData) 
#     dateString = CreateDateString()
#     figureOutputDirPath =  os.path.join(settings.BASE_DIR, dataDirPath,dateString) 

#     surveyData = []
#     with open(extractSurveyDataFilePath, 'rb') as f:
#        surveyData = pickle.load(f)   

#     if not os.path.exists(figureOutputDirPath):
#         os.mkdir(figureOutputDirPath)

#     figureCounter = 1
#     figureFilenameList = []

#     for question in surveyData:
#         # Skip the conscent question
#         if question.questionName == 'Consent': continue
       
#         if question.questionType['type'] not in questionHandleDict.keys():
#             print('[ERROR]: Unknown question type: ', question.questionType['type'])
#         else:             
#             # Generate the file path and save it to the list
#             figureFilePathBase = GenerateFigureFilePathBase(dateString,figureCounter,figureOutputDirPath)
#             figureFilenameList.append(figureFilePathBase)
#             figureCounter += 1 
             
#             # call the corresponding Question Handler to questionType
#             questionHandleDict[question.questionType['type']](question,figureFilePathBase)
        
#             # generate a word cloud if there is a free text portion of the question
#             if len(question.freeText) > 0:
#                 figureFilePathBase = GenerateFigureFilePathBase(dateString,figureCounter,figureOutputDirPath)
#                 figureFilenameList.append(figureFilePathBase)
#                 figureCounter += 1 
                
#                 VisualizeOtherTextQuestion(question, figureFilePathBase)
                        
#     saveReport2Db(figureFilenameList, report)
    
##################################################################################################################################

##################################################################################################################################
# This function returns a list of unique questions from the userResponse QuerySet generated by a frontend query
##################################################################################################################################
def GetListOfUniqueQuestions(userResponseQuerySet):
    questionList = []
    
    questionIDs = userResponseQuerySet.order_by().values_list('questionID').distinct()
    
    for qID in questionIDs:
        questionQuerySet = QuestionTable.objects.filter(id=qID[0])
        
        if len(questionQuerySet) == 1:
            questionList.append(questionQuerySet.first())
    
    return questionList

##################################################################################################################################
# This function returns a list responses to the question passed as an arguement
##################################################################################################################################
def GetUserResponsesToQuestion(question, userResponseQuerySet):
    
    userResponseList = []
    
    responsesToQuestion = userResponseQuerySet.filter(questionID=question.id)
    
    for response in responsesToQuestion:
        userResponseList.append(response)
        
    return userResponseList

##################################################################################################################################
# This function can be used for testing the data visualizer
##################################################################################################################################
questionHandleDict ={   'Slider':VisualizeSliderQuestion,
                        'MC':VisualizeMultipleChoiceQuestion,
                        'TE':VisualizeOpenTextQuestion}

def run(*arg):
    
    # make sure the tmp folder for storing the generated images exists
    isExist = os.path.exists(FIGURE_FOLDER_PATH)
    if not isExist:
        os.makedirs(FIGURE_FOLDER_PATH)
    
    # create a front end query to get some data from the DB
    aQuery = FrontEndQuery()   
    aQuery.date = '2023-01-01'
    #aQuery.locations = 'AB'

    userResponseQuerySet = HandleFrontEndQuery(aQuery)
    
    questionList = GetListOfUniqueQuestions(userResponseQuerySet)
    
    for question in questionList:
        userResponseList = GetUserResponsesToQuestion(question, userResponseQuerySet)
    
        if question.questionType not in questionHandleDict.keys():
            print('[ERROR]: Unknown question type: ', question.questionType)
        else:             
            questionHandleDict[question.questionType](question,userResponseList)
        
  