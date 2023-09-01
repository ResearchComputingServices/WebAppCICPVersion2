import pandas as pd
import plotly.express as px

from scripts.Utils import *
from scripts.DataVizualizers.VizUtils import *


import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from textwrap import fill
import matplotlib.patches as mpatches
##################################################################################################################################
#
##################################################################################################################################
def VisualizeRankOrderQuestion( question, 
                                userResponses,
                                numOfRespondents,
                                isEnglish = True,
                                saveToDirPath = TMP_FIGURE_FOLDER_PATH): 
    
    title = GetGraphicTitle(question, isEnglish)
    
    # Generate the responseDict (choiceID:average as the key:value pair) initially set the average to 0
    choiceQuerySet = ChoiceTable.objects.filter(questionID=question.id)
        
    totalResponses = numOfRespondents
    questionLabel = question.questionLabel
    
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

    #Added for creating a rank profile
    finalResponseDictsall = {}
    
    for key in responseDict:
        listOfRanks = responseDict[key]
        rankCount = {}
        
        for rank in listOfRanks:
            if rank == '1':
                if '1st' in rankCount.keys():
                    rankCount['1st'] += 1
                else:
                    rankCount['1st'] = 1
            elif rank == '2':
                if '2nd' in rankCount.keys():
                    rankCount['2nd'] += 1
                else:
                    rankCount['2nd'] = 1
            elif rank == '3':
                if '3rd' in rankCount.keys():
                    rankCount['3rd'] += 1
                else:
                    rankCount['3rd'] = 1
            else:
                if '4th +' in rankCount.keys():
                    rankCount['4th +'] += 1
                else:
                    rankCount['4th +'] = 1
    
        finalResponseDicts[key] = rankCount

    for key in responseDict:
        listOfRanks = responseDict[key]
        listOfRanks.sort(reverse = True)
        maxval = int(listOfRanks[0])
        rankCount = {}
        
        for rank in listOfRanks:
            if rank == '1':
                if '1st' in rankCount.keys():
                    rankCount['1st'] += maxval
                else:
                    rankCount['1st'] = maxval
            elif rank == '2':
                if '2nd' in rankCount.keys():
                    rankCount['2nd'] += maxval - 1
                else:
                    rankCount['2nd'] = maxval - 1
            elif rank == '3':
                if '3rd' in rankCount.keys():
                    rankCount['3rd'] += maxval - 2
                else:
                    rankCount['3rd'] = maxval - 2
            elif rank == '4':
                if '4th' in rankCount.keys():
                    rankCount['4th'] += maxval - 3
                else:
                    rankCount['4th'] = maxval - 3
            elif rank == '5':
                if '5th' in rankCount.keys():
                    rankCount['5th'] += maxval - 4
                else:
                    rankCount['5th'] = maxval - 4
            elif rank == '6':
                if '6th' in rankCount.keys():
                    rankCount['6th'] += maxval - 5
                else:
                    rankCount['6th'] = maxval - 5
            elif rank == '7':
                if '7th' in rankCount.keys():
                    rankCount['7th'] += maxval - 6
                else:
                    rankCount['7th'] = maxval - 6
            elif rank == '8':
                if '8th' in rankCount.keys():
                    rankCount['8th'] += maxval - 7
                else:
                    rankCount['8th'] = maxval - 7
            elif rank == '9':
                if '9th' in rankCount.keys():
                    rankCount['9th'] += maxval - 8
                else:
                    rankCount['9th'] = maxval - 8
            else:
                if str(maxval)+'th' in rankCount.keys():
                    rankCount[str(maxval)+'th'] += maxval - 9
                else:
                    rankCount[str(maxval)+'th'] = maxval - 9
    
        finalResponseDictsall[key] = rankCount

    
    
    # send everything to the figure creator
    return CreateStackedBarChart(   finalResponseDicts, 
                                    title,
                                    questionLabel,
                                    totalResponses,
                                    isEnglish,
                                    saveToDirPath),CreateRankChart(finalResponseDictsall, 
                                                                    title,
                                                                    questionLabel,
                                                                    totalResponses,
                                                                    isEnglish,
                                                                    saveToDirPath)
    
##################################################################################################################################
#
##################################################################################################################################

def CreateRankChart(responseDict,
                            graphicTitle,
                            questionLabel,
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
    
    #Sort to have the labels in order
    columns.sort()
    # create data frame with correct rows
    df = pd.DataFrame(columns=columns)
    
    
    # populate elements
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            value = responseDict[subQ][response]
            df.at[subQ, response] = value
            df.at[subQ, 'subQ'] = 0.
    #df.columns = ['subQ', '1st','2nd','3rd','4th +']
    #print(df.head(5))

    # normalize rows (magic, I dont know how this works)
    df['total'] = df.sum(axis=1)/numberOfResponses
    #df = df.multiply(100)
    #print(df.head(5))
    # change subQ to have the correct names
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            df.at[subQ, 'subQ'] = WrapText(subQ,15)
    
    df = df.sort_values(by=['total'], ascending=False)
    df = df.reset_index(drop=True)
    df = df[['subQ','total']]
    #print(df)

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

    # cmap = LinearSegmentedColormap.from_list('my_colours', colourMap)
        
    # Create the figure which plots the bar chart
    # creating the bar plot
    fig = plt.figure(figsize=(18,18))
    
    #Added comment for below line
    #plt.subplots_adjust(left=0.22)
    ax1 = plt.subplot2grid((10, 3), (0, 0), colspan=3, rowspan=9)
   
    # plot data in stack manner of bar type
    df.plot.bar(x='subQ', 
                y='total',            
            # kind='bar', 
            #stacked=True,
            ax=ax1,
            color=colourMap,
            rot = 0,
            legend=False)
            #bbox_to_anchor=(1.05,1))      
        
    
    #Modified to adjust the plots - Rohan
    plt.subplots_adjust(right=0.75)
    
    # ax1.set_title(graphicTitle,wrap=True,fontdict={'fontsize': 20, 'fontweight': 'medium'})
    ax1.set_title(graphicTitle+'/n',wrap=True,fontdict={'fontsize': 20, 'fontweight': 'medium',
 'horizontalalignment': 'center'},pad = 150.0,y=0.9)
    ax1.set_xticks(df.index)
    ax1.set_xticklabels(df.subQ, rotation=90)
    ax1.set_ylabel('')
    plt.xlabel(xlabel='')
    plt.yticks([]) 
    plt.xticks(fontsize=15)
    # plt.xticks(y_pos, objects,fontsize=15)
    #ax1.set_xticks([0,25,50,75,100])

    #Modified for the labels to display outside - Rohan
    # ax1.legend(bbox_to_anchor=(1.03,1))

    #Added by Priyanka  
    legend_handles = [plt.Line2D([0], [0], color=color, linewidth=5, label=label) for label, color in zip(['1','2','3','4','5','6','7','8'], colourMap)]
    ax1.legend(handles=legend_handles,bbox_to_anchor=(1.2,1),fontsize=13)
    
    # if isEnglish:
    #     ax1.set_xlabel('% of Responses',fontsize=15)
    # else:
    #     ax1.set_xlabel('% de réponses',fontsize=15)
       
    # Get the watermark image and add it to the figure
    waterMarkImg = image.imread(WATERMARK_IMAGE_FILE_PATH)
    # ax2 = fig.add_axes([0.,-0.1,0.2,0.2], anchor='NE', zorder=1)
    ax2 = fig.add_axes([0.0, 0.01, 0.15, 0.1], anchor='SW', zorder=1) 
    ax2.imshow(waterMarkImg)
    ax2.axis('off')

    # ax3 = fig.add_axes([0.75,0.01,0.25,0.1], anchor='NE', zorder=1)
    ax3 = fig.add_axes([0.75, 0.01, 0.2, 0.1], anchor='SE', zorder=1)
    reportDate = saveToDirPath.split("/")[-1] 
    aText = GetAnnotation(numberOfResponses, reportDate, isEnglish)
    annotateText = aText[0]+'\n'+aText[1]
    ax3.annotate(annotateText, xy=(1.,0.),xycoords='axes fraction',horizontalalignment='right',fontsize=15)
    ax3.axis('off')

    # plt.show() 

    # save the wordcloud to a file
    #Added by Priyanka
    questionLabel = questionLabel.split('_')[1]
    filename = questionLabel+'_'+str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX


    # filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format=GRAPHIC_FILE_TYPE)
    plt.close(fig)   
    
    return figureFilePath

def CreateStackedBarChart(  responseDict,
                            graphicTitle,
                            questionLabel,
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
    
    #Sort to have the labels in order
    columns.sort()
    # create data frame with correct rows
    df = pd.DataFrame(columns=columns)    
    
    # populate elements
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            value = responseDict[subQ][response]
            df.at[subQ, response] = value
            df.at[subQ, 'subQ'] = 0.
    #df.columns = ['subQ', '1st','2nd','3rd','4th +']
    #print(df.head(5))

    # normalize rows (magic, I dont know how this works)
    df = df.div(df.sum(axis=1), axis=0) 
    df = df.multiply(100)
    #print(df.head(5))
    # change subQ to have the correct names
    for subQ in responseDict.keys():
        for response in responseDict[subQ].keys():
            df.at[subQ, 'subQ'] = WrapText(subQ,15)
    #####################################################################
    # define colours to use
    # colourMap = [(0/255,0/255,0/255),
    #             #(233/255,28/255,36/255),
    #             (45/255,45/255,45/255),
    #             #(242/255,121/255,126/255),
    #             (151/255,151/255,151/255),
    #             (145/255,14/255,19/255),
    #             (51/255,51/255,51/255),
    #             (185/255,44/255,49/255)]

    colourMap = [(0/255,0/255,0/255),
            (45/255,45/255,45/255),
            (151/255,151/255,151/255),
            (145/255,14/255,19/255),
            (51/255,51/255,51/255),
            (185/255,44/255,49/255)]

    cmap = LinearSegmentedColormap.from_list('my_colours', colourMap)
        
    # Create the figure which plots the bar chart
    # creating the bar plot
    fig = plt.figure(figsize=(18,18))
   
    
    #Added comment for below line
    #plt.subplots_adjust(left=0.22)
    ax1 = plt.subplot2grid((12, 3), (0, 0), colspan=3, rowspan=9)
   
    # plot data in stack manner of bar type
    df.plot(x='subQ', 
            kind='barh', 
            stacked=True,
            ax=ax1,
            colormap=cmap)
            #bbox_to_anchor=(1.05,1))
    
    #Modified to adjust the plots - Rohan
    plt.subplots_adjust(right=0.75)
    
    # ax1.set_title(graphicTitle,wrap=True,fontdict={'fontsize': 19, 'fontweight': 'medium'},pad = 25.0)
    # ax1.set_ylabel('')
    # ax1.set_xticks([0,25,50,75,100])

    ax1.set_title(graphicTitle+'/n',wrap=True,fontdict={'fontsize': 20, 'fontweight': 'medium',
 'horizontalalignment': 'center'},pad = 150.0,y=0.85)
    ax1.set_ylabel('')
    ax1.set_xticks([0,25,50,75,100])
    plt.yticks(fontsize=15)
    plt.xticks(fontsize=15)

    #Modified for the labels to display outside - Rohan
    # ax1.legend(bbox_to_anchor=(1.03,1),fontsize=16)
    ax1.legend(bbox_to_anchor=(1,1),fontsize=13)

    if isEnglish:
        ax1.set_xlabel('% of Responses',fontsize=15)
    else:
        ax1.set_xlabel('% de réponses',fontsize=15)
       
    # Get the watermark image and add it to the figure
    waterMarkImg = image.imread(WATERMARK_IMAGE_FILE_PATH)
    # ax2 = fig.add_axes([0.,-0.1,0.2,0.2], anchor='NE', zorder=1)
    ax2 = fig.add_axes([0.05, 0.2, 0.15, 0.7], anchor='SW', zorder=1)
    ax2.imshow(waterMarkImg)
    ax2.axis('off')

    # ax3 = fig.add_axes([0.75,0.01,0.25,0.1], anchor='NE', zorder=1)
    reportDate = saveToDirPath.split("/")[-1] 
    aText = GetAnnotation(numberOfResponses, reportDate, isEnglish)
    annotateText = aText[0]+'\n'+aText[1]
    ax3 = fig.add_axes([0.75, 0.2, 0.2, 0.7], anchor='SE', zorder=1) 
    ax3.annotate(annotateText, xy=(1.,0.),xycoords='axes fraction',horizontalalignment='right',fontsize=15)
    ax3.axis('off')

    # plt.show() 

    # save the wordcloud to a file
    #Added by Priyanka
    questionLabel = questionLabel.split('_')[1]
    filename = questionLabel+'_'+str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX


    # filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    plt.savefig(figureFilePath, format=GRAPHIC_FILE_TYPE)
    plt.close(fig)   
    
    return figureFilePath
