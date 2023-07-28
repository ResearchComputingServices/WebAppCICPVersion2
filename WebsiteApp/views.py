from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from scripts.Utils import *
from scripts.Controller import HandleFrontEndQuery
from django.utils.translation import gettext,get_language
from datetime import datetime, timedelta
from django_tex.shortcuts import render_to_pdf
from WebAppCICPVersion2 import settings



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
    context['age_form_filter'] = AgeFilterForm()

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
       

        if theme[0] == 'Funding':
            theme[0] = 'FUN'
            frontEndQuery.questionThemes = theme
            
        elif theme[0] == 'Governance':
            theme[0] = 'GOV'
            frontEndQuery.questionThemes = theme
            
        elif theme[0] ==  'Policy':
            theme[0] =  'POL'
            frontEndQuery.questionThemes = theme
            
        elif theme[0] == 'Collaboration':
            theme[0] = 'COL'
            frontEndQuery.questionThemes = theme
            
        elif theme[0] == 'Challenges':
            theme[0] = 'CHA'
            frontEndQuery.questionThemes = theme
            
        elif theme == 'EDI':
            theme ='EDI'
            frontEndQuery.questionThemes = theme

        elif theme == 'Other':
            theme = 'OTH'
            frontEndQuery.questionThemes = theme
        
        else:
             frontEndQuery.questionThemes = theme

    elif theme is None:
        frontEndQuery.date = str(get_wed_date(date))

        friday_text_date, wednesday_text_date = dateInitialization(False,date)

        context['friday_text_date'] = friday_text_date
        context['wednesday_date'] = wednesday_text_date

    frontEndQuery.locations = context['locations'] = request.GET.getlist('province')


    frontEndQuery.languagePreference = context['languagePreference'] = request.GET.getlist('language')
    frontEndQuery.organizationSizes = context['orgSizes'] = request.GET.getlist('size')
    frontEndQuery.age = context['age'] = request.GET.getlist('age')
    frontEndQuery.qualtricsSurveyID = ''
    frontEndQuery.siteLanguage = get_language()

    if frontEndQuery:
        query_response_imagefilepaths, query_response_csv, errors = HandleFrontEndQuery(
            frontEndQuery)
        
         
    return  query_response_imagefilepaths, query_response_csv, errors,context
        


def landingPageView(request):


    context, frontEndQuery = formInitialization() 
   
    questionTheme = request.GET.getlist('theme')
    reportDate = request.GET.get('report_date')


    if len(questionTheme) != 0:
        query_response_imagefilepaths, query_response_csv, errors,context = themeOrDate(request, theme=questionTheme, date=None)

        context['filtered'] = 'filteredReport' 

        if questionTheme[0] == 'FUN':
            context['questionTheme'] = gettext('Funding')
            
        if questionTheme[0] == 'GOV':
            context['questionTheme'] = gettext('Governance')
            
        if questionTheme[0] == 'POL':
            context['questionTheme'] = gettext('Policy')
            
        if questionTheme[0] == 'COL':
            context['questionTheme'] = gettext('Collaboration')
            
        if questionTheme[0] == 'CHA':
            context['questionTheme'] = gettext('Challenges')
            
        if questionTheme[0] == 'EDI':
            context['questionTheme'] = gettext('EDI')

        if questionTheme[0] == 'OTH':
            context['questionTheme'] = gettext('Other')
        
        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:
            context["image_filepaths"] = query_response_imagefilepaths

            # Create a dat file to print the report
            image_dict = {}
            for i, filepath in enumerate(query_response_imagefilepaths, 1):
                            key = f"Figure{i}"
                            image_dict[key] = settings.BASE_ROOT+filepath
            datfilepath = settings.BASE_DIR /'WebsiteApp/templates/latexgraphics.dat'
            try:
                with open(datfilepath, "w") as f:
                    for key in image_dict.keys():
                        f.write(f"{key},{image_dict[key]}\n")
            except FileNotFoundError:
                print("Dat file not found")

        return render(request, 'index.html', context)
        

    elif reportDate:

        if reportDate == "2022-12-23" or reportDate== "2022-12-30" :
            info = gettext(" 🥳🥳🥳 HAPPY HOLIDAYS  NO REPORT PUBLISHED DURING THIS WEEK 🥳🥳🥳")
            context['info'] = info

            return render(request, 'index.html', context)
        
        else:

            query_response_imagefilepaths, query_response_csv, errors,context = themeOrDate(request, None,reportDate)

            friday_text_date, wednesday_text_date = dateInitialization(False,reportDate) 

            context['filtered'] = 'filteredReport'
            context['friday_text_date'] = friday_text_date
            context['wednesday_date'] = wednesday_text_date
            context['reportDate'] = reportDate

            if len(errors) != 0:
                context["errors"] = errors

            if len(query_response_imagefilepaths) != 0:
                context["image_filepaths"] = query_response_imagefilepaths

            # Create a dat file to print the report
            image_dict = {}
            for i, filepath in enumerate(query_response_imagefilepaths, 1):
                            key = f"Figure{i}"
                            image_dict[key] = settings.BASE_ROOT+filepath
                            
            datfilepath = settings.BASE_DIR /'WebsiteApp/templates/latexgraphics.dat'

            try:
                with open(datfilepath, "w") as f:
                    for key in image_dict.keys():
                        f.write(f"{key},{image_dict[key]}\n")
            except FileNotFoundError:
                print("Dat file not found")

            return render(request, 'index.html', context)
         
    else:
            if reportDate == None and len(questionTheme) == 0:
                return render(request, 'lpage.html', context)


def printReport(request):

    template_name = 'main.tex'
    context = {}
    # Call render_to_pdf function and capture the output
    pdf_output = render_to_pdf(request, template_name, context, filename='my_report.pdf')

    # Print the PDF output (This will also show logs generated during the rendering process)
    print(pdf_output)

    return pdf_output

##################################################################################################################################
# Calculates Wednesday based on Friday date
def get_wed_date(fri_date):
   
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
        


