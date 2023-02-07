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

def GetAnnotation(numberOfResponses, isEnglish):
    
    annotationText = ''
    
    if isEnglish:
        annotationText = '# of Responses: '+str(numberOfResponses)
    else:
        annotationText = '# de Réponses: '+str(numberOfResponses)    

    return annotationText

##################################################################################################################################
#
##################################################################################################################################

def SaveFigure(fig):
    
    fig = AddWaterMarkImage(fig)
    
    filename = str(uuid.uuid4())
    figureFilePath = os.path.join(FIGURE_FOLDER_PATH, filename)
    
    fig.write_image(figureFilePath,format='png',engine='kaleido')

    return filename

##################################################################################################################################
#
##################################################################################################################################

def AddAnnotation(fig, numberOfResponses, isEnglish):
    # Annotation Text
    annotationText = GetAnnotation(numberOfResponses, isEnglish)

    fig.add_annotation( text = annotationText, 
                        showarrow=False,
                        xref = 'paper',
                        yref = 'paper',
                        x = 1.,
                        y = 1.1)

    return fig

##################################################################################################################################
#
##################################################################################################################################

def AddWaterMarkImage(fig):
    fig.add_layout_image(
        dict(
            source=WATERMARK_IMAGE_FILE_PATH,
            xref="paper",
            yref="paper",
            x=0.,
            y=1.,
            sizex=0.25,
            sizey=0.25,
            layer="above")
        )
    
    return fig