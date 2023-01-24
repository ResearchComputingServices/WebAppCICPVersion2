import os

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
    acronym = ''
    
    if(provinceName == 'Québec'or provinceName == 'QC'):
        acronym = 'QC'
    elif(provinceName == 'New Brunswick'):
        acronym = 'NB'
    elif(provinceName == 'Ontario' or provinceName == 'Ontario (ON)' or provinceName == 'ON'):
        acronym = 'ON'
    elif(provinceName == 'British Columbia' or provinceName == 'BC' ):
            acronym = 'BC'
    elif(provinceName == 'Manitoba'or provinceName == 'MB'):
            acronym = 'MB'
    elif(provinceName == 'Nova Scotia'or provinceName == 'NS'):
            acronym = 'NS'
    elif(provinceName == 'Saskatchewan'or provinceName == 'SK'):
            acronym = 'SK'
    elif(provinceName == 'Alberta'or provinceName == 'AB'):
            acronym = 'AB'
    elif(provinceName == 'Prince Edward Island'or provinceName == 'PE'):
            acronym = 'PE'
    elif(provinceName == 'Yukon'):
            acronym = 'YK'
    else:
        acronym = 'Unknown'

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

        
                
    