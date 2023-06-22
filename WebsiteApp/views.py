from django.forms import ValidationError
from django.shortcuts import render
from .forms import *
from scripts.Utils import *
from scripts.Controller import HandleFrontEndQuery
from django.utils.translation import gettext,get_language
from datetime import datetime, timedelta
from django.contrib.sessions.backends.db import SessionStore

##################################################################################################################################
# Create your views here.

# For testing new code

def formInitialization():

    frontEndQuery = FrontEndQuery()
    context = {}

    context['themeFilter'] = ThemeFilterForm()
    context['dateFilter'] = DateFilterForm()
    context['province_form_filter'] = ProvinceFilterForm()
    context['language_form_filter'] = LanguageFilterForm()
    context['org_size_form_filter'] = OrgsizeFilterForm()

    return context, frontEndQuery

def dateInitialization(latestReport,dateSearchReport):

    if latestReport: 
        # Get the latest Friday date from today and Format the date from Y%-%m-%d to respective english and french formats in text
        friday_text_date = textdate(
            str(get_fridaydate_from_todays_date(datetime.now())), lang=get_language())
        wednesday_text_date = textdate(str(get_wed_date(
            str(get_fridaydate_from_todays_date(datetime.now())))), lang=get_language())
        
    elif len(dateSearchReport) != 0:
        friday_text_date = textdate(
            str(dateSearchReport), lang=get_language())
        wednesday_text_date = textdate(str(get_wed_date(
           dateSearchReport)), lang=get_language())

    return friday_text_date,wednesday_text_date
         

def latest_report(request):

    context, frontEndQuery = formInitialization()
    friday_text_date, wednesday_text_date = dateInitialization(True,'')

    context['friday_text_date'] = friday_text_date
    context['wednesday_date'] = wednesday_text_date

    # Pass the wednesday date to select the images from media folder
    frontEndQuery.date = str(get_wed_date(
        str(get_fridaydate_from_todays_date(datetime.now()))))
    frontEndQuery.siteLanguage = get_language()

    if frontEndQuery:
        query_response_imagefilepaths, query_response_csv, errors = HandleFrontEndQuery(
            frontEndQuery)

        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:

            context["image_filepaths"] = query_response_imagefilepaths

    return render(request, 'index.html', context)

# Function to render two different pages for theme and date


def themeOrDate(request, theme, date):

    context, frontEndQuery = formInitialization()

    if date is None:
        frontEndQuery.questionThemes = theme

    elif theme is None:
        
        if date is None:
             selected_date = request.COOKIES.get('selected_date')
             frontEndQuery.date = str(get_wed_date(selected_date))
        else:
            frontEndQuery.date = str(get_wed_date(date))

        friday_text_date, wednesday_text_date = dateInitialization(False,date)

        context['friday_text_date'] = friday_text_date
        context['wednesday_date'] = wednesday_text_date

    frontEndQuery.locations = request.GET.getlist('province')
    frontEndQuery.languagePreference = request.GET.getlist('language')
    frontEndQuery.organizationSizes = request.GET.getlist('size')
    frontEndQuery.qualtricsSurveyID = ''
    frontEndQuery.siteLanguage = get_language()

    if frontEndQuery:
        query_response_imagefilepaths, query_response_csv, errors = HandleFrontEndQuery(
            frontEndQuery)
         
    return  query_response_imagefilepaths, query_response_csv, errors
        

def landingPageView(request):


    context, frontEndQuery = formInitialization() 
    context['filtered'] = 'filteredReport'
    
   
    questionTheme = request.GET.getlist('theme')
    reportDate = request.GET.get('report_date')


    if len(questionTheme) != 0:
        query_response_imagefilepaths, query_response_csv, errors = themeOrDate(request, theme=questionTheme, date=None)

        
        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:
            context["image_filepaths"] = query_response_imagefilepaths

        response = render(request, 'index.html', context)

        return response
        

    elif reportDate:

        query_response_imagefilepaths, query_response_csv, errors = themeOrDate(request, None,reportDate)

        friday_text_date, wednesday_text_date = dateInitialization(False,reportDate)

        context['friday_text_date'] = friday_text_date
        context['wednesday_date'] = wednesday_text_date
        
        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:
            context["image_filepaths"] = query_response_imagefilepaths

        return render(request, 'index.html', context)
         
    else:
             
        return render(request, 'lpage.html', context)
    
##################################################################################################################################
# Calculates Wednesday based on Friday date
def get_wed_date(fri_date):
    print(fri_date)
    fri_date = datetime.strptime(fri_date, '%Y-%m-%d')
    wed_date = fri_date + \
                timedelta(days = -2)
    return wed_date.date()

# Converts the Date from %Y-%m-%d to Month Date, Year
def textdate(date,lang):

    date = datetime.strptime(date, '%Y-%m-%d')
    
    if lang == "fr":
        fr_date_text = date.strftime("%b %d, %Y")
        return fr_date_text
       
    else:
        en_date_text = date.strftime("%d %B, %Y")

        return en_date_text

##################################################################################################################################
# Fetching the Friday date based on user input date
def get_fridaydate_from_todays_date(todays_date):
        

# Using current time
        week_day = todays_date.weekday()

        #Monday
        if week_day == 0:
                # Prev Friday
                past_week_friday = todays_date + \
                                timedelta(days = -3)
                return(past_week_friday.date())   
                    
        #Tuesday                        
        elif week_day == 1:
                # Prev Friday
                past_week_friday = todays_date + \
                                timedelta(days = -4)
                return(past_week_friday.date())
        
        #Wednesday                        
        elif week_day == 2:
                
                # Prev Friday 
                past_week_friday = todays_date + \
                                timedelta(days = -5)
                return(past_week_friday.date())
        
        #Thursday                        
        elif week_day == 3:
                
                # Prev Friday
                past_week_friday = todays_date + \
                                timedelta(days = -6)
                return(past_week_friday.date())
        
        #Friday                        
        elif week_day == 4:
                # Today - Friday
                this_week_friday = todays_date + \
                                timedelta(days = 0)
                return(this_week_friday.date())
        
        #Saturday
        elif week_day == 5:
                # Present Week Friday
                this_week_friday = todays_date + \
                                timedelta(days = -1)
                return(this_week_friday.date())
        
        #Sunday                        
        elif week_day == 6:
                # Present Week Friday
                this_week_friday = todays_date + \
                                timedelta(days = -2)
                return(this_week_friday.date())