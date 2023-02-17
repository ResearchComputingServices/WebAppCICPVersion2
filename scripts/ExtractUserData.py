import os
import re

from scripts.Utils import *
from InteractiveDB.models import UserTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# 
##################################################################################################################################  
def GetSize(numberOfEmployees):
     
    size = 'None'
    
    if(numberOfEmployees < 10):
        size = 'small'
    elif(numberOfEmployees < 25):
        size = 'medium'
    else:
        size = 'large'   
    
    return size

##################################################################################################################################
# 
##################################################################################################################################  
def GetProvineAcronym(provinceName):
    provinceName = provinceName.strip().lower()
    provinceName = re.sub(r'[^\w\s]','',provinceName)
    
    acronym = ''
    
    if 'québec' in provinceName or 'quebec' in provinceName or 'QC' in provinceName or 'qc' in provinceName:
        acronym = 'QC'
    elif 'New Brunswick' in provinceName or 'new brunswick' in provinceName or 'nb' in provinceName or 'NB' in provinceName:
        acronym = 'NB'
    elif 'Ontario' in provinceName or  'Ontario (ON)' in provinceName or 'ON' in provinceName or 'on' in provinceName:
        acronym = 'ON'
    elif 'british columbia' in provinceName or 'BC' in provinceName or 'bc' in provinceName:
            acronym = 'BC'
    elif 'manitoba' in provinceName or 'MB' in provinceName or 'mb' in provinceName:
            acronym = 'MB'
    elif 'nova scotia' in provinceName or 'NS' in provinceName or 'ns' in provinceName:
            acronym = 'NS'
    elif 'aaskatchewan' in provinceName or 'SK' in provinceName or 'sk' in provinceName:
            acronym = 'SK'
    elif 'alberta' in provinceName or 'AB' in provinceName or 'ab' in provinceName:
            acronym = 'AB'
    elif 'prince edward island' in provinceName or 'pe' in provinceName or 'PEI' in provinceName or 'pei' in provinceName:
            acronym = 'PE'
    elif 'yukon' in provinceName or 'YK' in provinceName or 'yk' in provinceName:
            acronym = 'YK'
    elif 'newfoundland' in provinceName or 'nlf' in provinceName or 'nl' in provinceName:
            acronym = 'NL'
    elif 'northwest territories' in provinceName or 'nwt' in provinceName or 'nt' in provinceName:
            acronym = 'NT'
    else:
        acronym = 'XX'

    return acronym

##################################################################################################################################
# 
##################################################################################################################################  
def GetNumber(token):
    num = 0
    
    if token != '':
        num = int(token)
    
    return num

##################################################################################################################################
# Main function 
##################################################################################################################################  

def run(*args):
    
    userDataFilePath = os.path.join(settings.BASE_DIR, 
                                    settings.DATA_DIR_PATH, 
                                    settings.USER_DATA_FILENAME)

    
    userDataFile = open(userDataFilePath, 'r')
    lines = userDataFile.readlines()
    
    for line in lines:
        tokens = line.split('^')
        
        FT = GetNumber(tokens[7])
        PT = GetNumber(tokens[8])
        VT = GetNumber(tokens[9])
               
        user = UserTable()
        
        user.externalDataReference = tokens[3]
        user.domain = 'philatronic'
        user.province = GetProvineAcronym(tokens[10])
        user.size = GetSize(FT+PT+VT)
        user.languagePreference = tokens[6]
        
        user.save()

        
                
    