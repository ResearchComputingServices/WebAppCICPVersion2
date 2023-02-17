import os
from datetime import date, datetime
import time

from scripts.Utils import IMAGE_LIFE_TIME_SECONDS, FIGURE_FOLDER_PATH

def run(*args): 
    currentTime = float(time.time())
    
    for filename in os.listdir(FIGURE_FOLDER_PATH):
        filePath = os.path.join(FIGURE_FOLDER_PATH, filename)
        
        if os.path.isfile(filePath):
            creationTime = os.path.getctime(filePath)
            deltaTime = currentTime - creationTime
            
            if deltaTime > IMAGE_LIFE_TIME_SECONDS:
                os.remove(filePath)
                print('Delete: ',filePath)
            else:
                print('Keep: ', filePath)
