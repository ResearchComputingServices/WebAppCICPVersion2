import os
import uuid
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
from googletrans import Translator

from scripts.Utils import *

##################################################################################################################################
#
##################################################################################################################################

def GetGraphicTitle(question, isEnglish):
    title = ''
    if isEnglish:
        title = question.questionTextEnglish
    else:
        title = question.questionTextFrench

    return title.strip()

##################################################################################################################################
#
##################################################################################################################################

def GetAnnotation(numberOfResponses,reportDate, isEnglish):
    
    annotationText = ['','','']
    
    if isEnglish:
        annotationText[0] = 'Number of Responses: '+str(numberOfResponses)
        annotationText[1] = 'Results of survey distributed on : ' + reportDate
        annotationText[2] = 'Plot Details:'
    else:
        annotationText[0] = 'Nombre de Réponses: '+str(numberOfResponses)   
        annotationText[1] = "Résultats de l'enquête distribués on : " + reportDate
        annotationText[2] = 'Détails du terrain:'

    return annotationText

##################################################################################################################################
#
##################################################################################################################################

def SaveFigureBar(xMin,fig,
               saveToDirPath=TMP_FIGURE_FOLDER_PATH):
    
    fig = AddWaterMarkImageBar(xMin,fig)
    
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    
    fig.write_image(figureFilePath,format=GRAPHIC_FILE_TYPE,engine='kaleido')

    return figureFilePath


def SaveFigure(fig,
               saveToDirPath=TMP_FIGURE_FOLDER_PATH):
    
    fig = AddWaterMarkImage(fig)
    
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    
    fig.write_image(figureFilePath,format=GRAPHIC_FILE_TYPE,engine='kaleido')

    return figureFilePath

def SaveFigurePie(  fig,
                    saveToDirPath=TMP_FIGURE_FOLDER_PATH):
    
    fig = AddWaterMarkImagePie(fig)
    
    filename = str(uuid.uuid4())+GRAPHIC_FILE_SUFFIX
    figureFilePath = os.path.join(saveToDirPath, filename)
    
    fig.write_image(figureFilePath,format=GRAPHIC_FILE_TYPE,engine='kaleido')

    return figureFilePath
    


##################################################################################################################################
#
##################################################################################################################################

def AddAnnotation(fig, numberOfResponses, reportDate, isEnglish):
    # Annotation Text
    annotationText = GetAnnotation(numberOfResponses,reportDate, isEnglish)

    fig.add_annotation(text=annotationText[0],
                       showarrow=False,
                       xanchor='right',
                       yanchor='top',
                       x=1.25,
                       y=1,
                       font=dict(size=15, color='black'))
    
    fig.add_annotation( text =  annotationText[1], 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = 0.5,
                        y = -0.1,
                        font=dict(size=15, color='black'))
    return fig


def AddAnnotationBar(fig, numberOfResponses, reportDate, isEnglish, xMin,xMax):
    # Annotation Text
    annotationText = GetAnnotation(numberOfResponses,reportDate, isEnglish)

    fig.add_annotation(text=annotationText[2],
                       showarrow=False,
                       xref = 'paper',
                       yref = 'paper',
                       x = xMin,
                       y= -0.42,
                       font=dict(size=18, color='black',family='Roboto, sans-serif'))
    
    fig.add_annotation( text =  annotationText[0], 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = xMin,
                        y = -0.47,
                        font=dict(size=15, color='black'))

    fig.add_annotation( text =  annotationText[1], 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = xMin,
                        y = -0.52,
                        font=dict(size=15, color='black'))

    return fig

##################################################################################################################################
#
##################################################################################################################################

def AddWaterMarkImageBar(xMin,fig):
    fig.add_layout_image(
        dict(
            source=WATERMARK_IMAGE_FILE_PATH,
            xref="paper",
            yref="paper",
            x=xMin,
            y=-0.25,
            sizex=0.25,
            sizey=0.25,
            layer="below")
        )
    
    return fig

def AddWaterMarkImage(fig):
    fig.add_layout_image(
        dict(
            source=WATERMARK_IMAGE_FILE_PATH,
            xref="paper",
            yref="paper",
            x=0.2,
            y=-0.2,
            sizex=0.25,
            sizey=0.25,
            layer="below",
            xanchor="left",
            yanchor="bottom")
        )
    
    return fig

def AddWaterMarkImagePie(fig):
    fig.add_layout_image(
        dict(
            source=WATERMARK_IMAGE_FILE_PATH,
            xref="paper",
            yref="paper",
            x=0.31,
            y=0.5,
            sizex=0.35,
            sizey=0.35,
            layer="below",
            xanchor="left",
            yanchor="bottom")
        )
    
    return fig

##################################################################################################################################
# This function is a helper function for the translation of text from french to english and vice versa
##################################################################################################################################

def removeStopWords(text, language):
    
    filteredText = []

    textTokens = word_tokenize(text)

    listOfStopWords = stopwords.words(language)
        
    for word in textTokens:
        if word.lower() not in listOfStopWords:
            filteredText.append(word.lower())

    return filteredText

def RemoveStopWords(text):

    filteredText = removeStopWords(text, 'english')
    filteredText = removeStopWords(text, 'french')

    return filteredText

##################################################################################################################################
# This function returns translated text from srcCode to destCode 
##################################################################################################################################

def SplitText(inputText, maxLength = 10000):
    
    textList = []

    textTokens = word_tokenize(inputText)
    
    currentString = ''
    for word in textTokens:
        if len(currentString) < maxLength:
            currentString = currentString + ' ' + word    
        else:
            textList.append(currentString)
            currentString = ''

    return textList


def Translate(inputText, srcCode, destCode):
    
    outputText = ''
            
    translator = Translator()
 
    # There is a limit of 15k characters at a time so longer blocks of text will need to be split up
    textList = []
    
    if len(inputText) > 15000: 
        textList = SplitText(inputText)
    else:
        textList.append(inputText)
 
    for text in textList:
        result = translator.translate(text,src=srcCode,dest=destCode)
        outputText = outputText + ' ' + result.text
    
    return outputText

##################################################################################################################################
# This is a helper function for the CreateWordCloud function. It returns the text responses in either french or english depending
# on the value of destCode ('en', or 'fr')
##################################################################################################################################

def GetTextForWordCloud(responseText, destCode):
       
    resultingText = ''
    
    srcCode = 'en'
    if destCode == 'en':
        srcCode = 'fr'
    
    if len(responseText) != 0:
        translatedText = Translate(responseText, srcCode, destCode)   
        stopwordsFiltered = RemoveStopWords(translatedText) 
        resultingText = ' '.join(stopwordsFiltered)
    else:
        print('[ERROR]: GetTextForWordCloud: responseText empty.')
    
    return resultingText