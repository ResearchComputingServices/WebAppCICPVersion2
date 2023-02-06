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
#
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
#
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
def CreateSubQuestionResponseDict(listOfUserResponses):
    subQResponseDict = {}
    
    for response in listOfUserResponses:
        if response in subQResponseDict.keys():
            subQResponseDict[response] += 1
        else:
            subQResponseDict[response] = 1
    
    return subQResponseDict

def VisualizeMatrixQuestion(question, 
                            userResponses,
                            isEnglish = True): 
    # only the Parent Matrix question should be included in the list to be visualized
    if question.parentQuestionID != None:
        return
    
    title = ''
    if isEnglish:
        title = question.questionTextEnglish
    else:
        title = question.questionTextFrench
    
    responseDict= {}
            
    # Get all the subquestions
    subQuestionsQuerySet = QuestionTable.objects.filter(parentQuestionID=question)
    
    totalResponses = len(userResponses)
    
    for r in userResponses:
        subQ = subQuestionsQuerySet.filter(id=r.questionID.id).first()
        
        if subQ.questionTextEnglish in responseDict.keys():
            choice = ChoiceTable.objects.filter(questionID=subQ.id, recode = r.answerValue).first()
            
            responseDict[subQ.questionTextEnglish].append(choice.choiceTextEnglish)
        else:
            responseDict[subQ.questionTextEnglish] = []
    
    # need to turn the responseDict into a dictionary of dictionarys.
    # first dictionary key value pair is subQustionText:dict_2
    # the next dictionary (dict_2) has key:value pair responseText:count
    finalResponseDicts = {}
    for key in responseDict:
       dict = CreateSubQuestionResponseDict(responseDict[key])
       finalResponseDicts[key] = dict
       
    for key in finalResponseDicts.keys():
        print(key,':', finalResponseDicts[key])
    
    filename = str(uuid.uuid4())
    CreateStackedBarChart(finalResponseDicts, 
                          title,
                          totalResponses,  
                          os.path.join(FIGURE_FOLDER_PATH, filename))

##################################################################################################################################
#
##################################################################################################################################

def CreateStackedBarChart(  responseDict,
                            graphicTitle,
                            numberOfResponses,
                            figureFilePath,
                            isEnglish = True):
    
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
    
    # Annotation Text
    annotationText = ''
    if isEnglish:
        annotationText = '# of Responses: '+str(numberOfResponses)
    else:
        annotationText = '# de Réponses: '+str(numberOfResponses)

    # Get the title
    graphicTitle = WrapText(graphicTitle)       
   
    
    # create the actual plot object
    fig = px.bar(   df, 
                    color="response", 
                    y="subQ", 
                    x="value", 
                    title=graphicTitle,
                    color_discrete_sequence=colourMap,
                    orientation='h',
                    width=FIGURE_WIDTH_PX,
                    height=FIGURE_HEIGHT_PX)
    
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)      
    
    # update the layout of the figure
    fig.update_layout(  font_family='Helvetica Now', 
                        font_color="black",
                        plot_bgcolor='rgb(232,232,232)',
                        title_font={'size': 20})
        
    fig.add_annotation( text = annotationText, 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = 1.,
                        y = 1.1)

    fig.write_image(figureFilePath,format='png',engine='kaleido')

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

    fig.add_annotation( text = annotationText, 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = 1.,
                        y = 1.1)

    fig.write_image(figureFilePath,format='png',engine='kaleido')
    
##################################################################################################################################
# This function returns a list of unique questions from the userResponse QuerySet generated by a frontend query
##################################################################################################################################
def GetListOfUniqueQuestions(userResponseQuerySet):
    questionList = []
    
    # Get all the unique questions in the set of responses
    questionIDs = userResponseQuerySet.order_by().values_list('questionID').distinct()
    
    # use the unique questionIDs to get a list of the questions
    for qID in questionIDs:
        questionQuerySet = QuestionTable.objects.filter(id=qID[0])
        
        if len(questionQuerySet) == 1:
            question = questionQuerySet.first()

            # handle matrix questions differently because they have subQuestions    
            if question.questionType == MATRIX_QUESTION:
                parentQuestion = QuestionTable.objects.filter(id=question.parentQuestionID.id).first()
                if parentQuestion not in questionList:
                    questionList.append(parentQuestion) 
            else:            
                questionList.append(question)   
    
    return questionList

##################################################################################################################################
# This function returns a list responses to the question passed as an arguement
##################################################################################################################################
def GetUserResponsesToQuestion(question, userResponseQuerySet):
    
    userResponseList = []
    
    if question.questionType == MATRIX_QUESTION:
        subQuestionsQuerySet = QuestionTable.objects.filter(parentQuestionID=question)
        
        for subQuestion in subQuestionsQuerySet:
            responsesToQuestion = userResponseQuerySet.filter(questionID=subQuestion.id)
    
            for response in responsesToQuestion:
                userResponseList.append(response)
    else:
        responsesToQuestion = userResponseQuerySet.filter(questionID=question.id)
    
        for response in responsesToQuestion:
            userResponseList.append(response)
        
    return userResponseList

##################################################################################################################################
# This function can be used for testing the data visualizer
##################################################################################################################################
questionHandleDict ={   'Slider':VisualizeSliderQuestion,
                        'MC':VisualizeMultipleChoiceQuestion,
                        'TE':VisualizeOpenTextQuestion,
                        'Matrix':VisualizeMatrixQuestion}

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
        
  