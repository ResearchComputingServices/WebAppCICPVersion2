import os
import json

from scripts.Utils import *
from InteractiveDB.models import SurveyTable, QuestionTable, ChoiceTable, UserTable, UserResponseTable
from WebAppCICPVersion2 import settings


def run(*args):

    externalRefNum = '108172149RR0001'
    user = GetUser(externalRefNum) 
    print(user)