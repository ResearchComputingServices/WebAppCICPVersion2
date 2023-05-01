import os
import re

from scripts.Utils import *
from InteractiveDB.models import UserTable
from WebAppCICPVersion2 import settings

##################################################################################################################################
# This collection of functions interprets the raw input from the user database csv file and returns a value which is stored in
# a entry in the database User Table 
##################################################################################################################################

def GetLanguage(langToken):
    lang = None
    
    if langToken == 'FR-CA':
        lang = 'FR'
    elif langToken == 'EN':
        lang = 'EN'
    else:
        lang = ''
    
    return lang

##################################################################################################################################

    
def GetDesignation(desToken):
    
    desg = None
       
    if desToken in USER_DESIGNATION_DICT.keys():
        desg = USER_DESIGNATION_DICT[desToken]
    else:
        desg = ''
    
    return desg

##################################################################################################################################

def GetDomain(domainToken):
    domain = None
    
    if domainToken in USER_DOMAIN_DICT.keys():
        domain = USER_DOMAIN_DICT[domainToken]
    else:
        domain = ''
        
    return domain


##################################################################################################################################
    
def GetSubDomain(subDomToken):
    return ''

##################################################################################################################################
    
def GetLocationPolygon(locPolyToken):
    return ''

##################################################################################################################################
   
def GetUrbanRural(token):
    return ''

##################################################################################################################################
    
def GetSubsample(subToken):
    subSampleString = ''
    
    for id in USER_SUB_SAMPLE_IDS:
        if id in subToken:
            subSampleString = subSampleString + ',' + id
    
    return subSampleString

##################################################################################################################################
    
def GetDate(dateToken):
    dateString = ''

    dateTokenSplit = dateToken.split(' ')
    dateString = dateTokenSplit[0]
    
    if '#' not in dateString and len(dateString) > 0:
        dateString = dateString.replace('/','-')
        dateString = dateString.replace('.','-')
    
        dateSplit = dateString.split('-')

        if len(dateSplit[0]) != 4:
            if int(dateSplit[0]) <= 12:
                dateString = dateSplit[2]+'-'+dateSplit[0]+'-'+dateSplit[1]    
            else:
                dateString = dateSplit[2]+'-'+dateSplit[1]+'-'+dateSplit[0]   
    
    else:
        dateString = '1000-01-01'
    
    return dateString

##################################################################################################################################

def GetSize(numberOfEmployees):
     
    size = 'None'
    
    if(numberOfEmployees < 25):
        size = 'SM'
    elif(numberOfEmployees < 200):
        size = 'MD'
    else:
        size = 'LG'   
    
    return size

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
 
def GetNumber(token):
    num = 0
    
    if token != '':
        num = int(token)
    
    return num

##################################################################################################################################
# Main function
#  TOKENS:
# 0     Language
# 1     ExternalDataReference
# 2     Province
# 3     designation_code
# 4     registration_date
# 5     sub_category_code
# 6     category_code
# 7     Location Polygons
# 8     Urban/Rural
# 9     SubSample
# 10    FTE
# 11    Volunteers
# 12    PTE
# 13    Job Title
##################################################################################################################################  

def run(*args):
    
    userDataFilePath = os.path.join(settings.BASE_DIR, 
                                    settings.DATA_DIR_PATH, 
                                    settings.USER_DATA_FILENAME)

    
    userDataFile = open(userDataFilePath, 'r')
    lines = userDataFile.readlines()
        
    for line in lines:        
        # Get the tokens from the input line separated by ^ symbol
        tokens = line.split('^')     
        language = tokens[0]
        externalDataReference = tokens[1]
        province = tokens[2]
        designation_code = tokens[3]
        registration_date = tokens[4]
        sub_category_code = tokens[5]
        category_code = tokens[6]
        locationPolygons= tokens[7] 
        urbanRural = tokens[8]
        subSample = tokens[9]
        fte = GetNumber(tokens[10])
        volunteers = GetNumber(tokens[11])
        pte = GetNumber(tokens[12])
        jobTitle = tokens[13] 
        
        # Create an instance of the user model       
        user = UserTable()
        
        # store the tokens in the previously created instance of a user model       
        user.domain = GetDomain(category_code)
        user.subDomain = GetSubDomain(sub_category_code)
        user.subSample = GetSubsample(subSample)
        user.jobTitle = jobTitle
        
        user.languagePreference = GetLanguage(language)
        user.externalDataReference = externalDataReference
        user.designation = GetDesignation(designation_code)
        user.locationPolygon = GetLocationPolygon(locationPolygons)
        user.urbanRural = GetUrbanRural(urbanRural)
        user.province = GetProvineAcronym(province)
        user.dateFounded = GetDate(registration_date)
        user.size = GetSize(fte+pte+volunteers)

        user.save()   
                

