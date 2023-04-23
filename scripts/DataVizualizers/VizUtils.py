import os
import uuid

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

def SaveFigurePie(fig,
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