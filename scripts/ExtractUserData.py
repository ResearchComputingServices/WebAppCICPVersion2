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
    
    if langToken == 'FR-CA' or langToken == 'FR':
        lang = 'FR'
    elif langToken == 'EN':
        lang = 'EN'
    else:
        lang = 'EN'
    
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

        if int(dateSplit[2]) < 1990 :
            age = 'OLD'
        else:
            age = 'NEW'
    
    else:
        dateString = '1000-01-01'
        age = 'NULL'

    return dateString,age

##################################################################################################################################

def GetHumanResources(FTE,PTE,volunteers):
     
    HRType = 'None'
    
    if(FTE > 0 or PTE > 0):
        HRType = "PD"
    
    else:
        HRType = "VO"   
    
    return HRType

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

def GetExpenditure(expenditure):
    
    if float(expenditure) <= 145316:
        expenditure = "XS"  # Extra Small
    elif float(expenditure) <= 384330:
        expenditure = "SM"  # Small
    elif float(expenditure) <= 819386:
        expenditure = "MD"  # Medium
    elif float(expenditure) <= 2177639:
        expenditure = "LG"  # Large
    elif float(expenditure) <= 55838038:
        expenditure = "XL" # Extra Large
    elif float(expenditure) <= 364115081:
         expenditure = "XXL"  # Super Large
    else:
        expenditure = "XS" #Make it a zero by adding XS
    

    return (expenditure)

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
# 14    Region
# 15    Expenditure
##################################################################################################################################  
import pandas as pd

def run(*args):
    
    userDataFilePath = os.path.join(settings.BASE_DIR, 
                                    settings.DATA_DIR_PATH, 
                                    settings.USER_DATA_FILENAME)

    
    userDataFile = open(userDataFilePath, 'r')
    lines = userDataFile.readlines()

    df = pd.read_csv(userDataFilePath,sep='^',header=None,encoding='utf-8')
    df = df.fillna('')
    print(df.head())
        
    for index,line in df.iterrows(): 
        # Get the tokens from the input line separated by ^ symbol
        language = line[0]
        externalDataReference = line[1]
        province = line[2]
        designation_code = line[3]
        registration_date = line[4]
        sub_category_code = line[5]
        category_code = line[6]
        locationPolygons= line[7] 
        urbanRural = line[8]
        subSample = line[9]
        fte = GetNumber(line[10])
        volunteers = GetNumber(line[11])
        pte = GetNumber(line[12])
        jobTitle = line[13]
        region = line[14]
        expenditure = GetExpenditure(line[15])
        
       # Create an instance of the user model        
        user = UserTable()
        
        # store the tokens in the previously created instance of a user model       
        user.domain = GetDomain(category_code)
        user.subDomain = GetSubDomain(sub_category_code)
        user.subSample = GetSubsample(subSample)
        user.jobTitle = jobTitle
        user.region = region
        user.expenditure = expenditure
        
        user.languagePreference = GetLanguage(language)
        user.externalDataReference = externalDataReference
        user.designation = GetDesignation(designation_code)
        user.locationPolygon = GetLocationPolygon(locationPolygons)
        user.urbanRural = GetUrbanRural(urbanRural)
        user.province = GetProvineAcronym(province)
        user.dateFounded,user.age = GetDate(registration_date)
        user.size = GetSize(fte+pte+volunteers)
        user.hrtype = GetHumanResources(fte,pte,volunteers)

        user.save()   
                

