from django.shortcuts import render
from .forms import FilterForm
from scripts.Utils import *
from scripts.Controller import HandleFrontEndQuery
from django.utils.translation import gettext,get_language
from datetime import datetime, timedelta

##################################################################################################################################
# Create your views here.
def report_results_EN(request):
   
    # handle the case where the user has specified front end query options
    if request.GET:
        
        form_filter = FilterForm(request.GET)      
        context = {'form_filter' : form_filter}

<<<<<<< HEAD
        # Get the date and handle the case where no date is specified by the user
        date = request.GET.get('report_date', None)
=======

        # Date Format - Y%-%m-%d
        # Type - str
        date = request.GET.get('report_date', None)
        
        
>>>>>>> main
        if date is None:
            date = str(datetime.now().date())

        else:
<<<<<<< HEAD
            date_requested = request.GET['report_date']
            date_string = get_wed_date(date_requested, get_language())
            date = str(datetime.strptime(date_string, "%d %B, %Y").date())
        
        # Get the remainder of the the query requirements
        location = (request.GET.getlist('province'))
        question_theme = (request.GET.getlist('theme'))
        language_preference = request.GET.getlist('language')
        organization_size = (request.GET.getlist('size'))
        site_language = get_language()
=======
>>>>>>> main

            # Date Format - Y%-%m-%d
            # Type - str 
            # Input - Friday Date selected by the user
            user_requested_friday_date = request.GET['report_date']

<<<<<<< HEAD
        # Handle case where the specified date is in Special Date.
        if date in SPECIAL_DATE:
            info = gettext("🥳🥳🥳 HAPPY HOLIDAYS  NO REPORT PUBLISHED DURING THIS WEEK 🥳🥳🥳")
=======
            # Date Format - Y%-%m-%d
            # Type - str 
            # Input - Friday Date selected by the user
            # Output - Wednesday date that matches the folder created in Media
            user_response_images_wed_date = get_wed_date(user_requested_friday_date)
            print("user_response_images_wed_date",user_response_images_wed_date)

            location = (request.GET.getlist('province'))
            question_theme = (request.GET.getlist('theme'))
            language_preference = request.GET.getlist('language')
            organization_size = (request.GET.getlist('size'))

        if user_requested_friday_date == "2022-12-23" or user_requested_friday_date == "2022-12-30" :
            info = gettext(" 🥳🥳🥳 HAPPY HOLIDAYS  NO REPORT PUBLISHED DURING THIS WEEK 🥳🥳🥳")
>>>>>>> main
            context['info'] = info
        else:
<<<<<<< HEAD
            wednesday_date = get_wed_date(date_requested,lang=get_language())
            friday_text_date = get_fri_textdate(date_requested,lang=get_language())
=======
            
>>>>>>> main

            # Get the textdates to display in the frontend based on English and French selection
            wednesday_text_date = textdate(str(user_response_images_wed_date),lang=get_language())
            print("wednesday_text_date",wednesday_text_date)
            friday_text_date = textdate(str(user_requested_friday_date),lang=get_language())
            print("friday_text_date",friday_text_date)


            # Pass the dates in text format to the frontend
            context['wednesday_date'] = wednesday_text_date
            context['friday_text_date'] = friday_text_date

            front_end_query = FrontEndQuery()

            front_end_query.date = str(user_response_images_wed_date)
            front_end_query.locations = location
            front_end_query.questionThemes = question_theme
            front_end_query.languagePreference = language_preference
            front_end_query.organizationSizes = organization_size
            front_end_query.qualtricsSurveyID = ''
            front_end_query.siteLanguage = site_language
            
            if front_end_query:
                query_response_imagefilepaths,query_response_csv,errors = HandleFrontEndQuery(front_end_query)
                print(query_response_imagefilepaths)

                if len(errors) != 0:
                    context["errors"] = errors
            
                if len(query_response_imagefilepaths) != 0:
                    context["image_filepaths"] = query_response_imagefilepaths


        return render(request, 'index.html', context)

    # This handles the case where we need to display the default pages
    else:

        form_filter = FilterForm()

        
        # For default selection and display of latest report

        # Get the latest Friday date from today
        default_this_week_friday_date = str(get_fridaydate_from_todays_date(datetime.now()))
        print("default_this_week_friday_date",default_this_week_friday_date)

        # Format the date from Y%-%m-%d to respective english and french formats in text
        friday_text_date = textdate(str(default_this_week_friday_date),lang=get_language())
        print("friday_text_date inside else",friday_text_date)

        # Get the wednesday date to search in the media folder and display on the frontend
        # based on the Friday date
        wednesday_date = get_wed_date(default_this_week_friday_date)
        print("wednesday_date inside else",wednesday_date)

        # Format the date from Y%-%m-%d to respective english and french formats in text
        wednesday_text_date = textdate(str(wednesday_date),lang=get_language())
        print("wednesday_text_date inside else", wednesday_text_date)

        context = {'form_filter' : form_filter,'friday_text_date' : friday_text_date,'wednesday_date' : wednesday_text_date}
        front_end_query = FrontEndQuery()

<<<<<<< HEAD
        date_requested = str(get_fridaydate_from_todays_date(datetime.now()))
        date_string = get_wed_date(date_requested, get_language())
        print(type(date_string))
        date = datetime.strptime(date_string, "%d %B, %Y").date()
        front_end_query.date = str(date)
=======

        # Pass the wednesday date to select the images from media folder
        front_end_query.date = str(wednesday_date)
>>>>>>> main
      
        if front_end_query:
                query_response_imagefilepaths,query_response_csv,errors = HandleFrontEndQuery(front_end_query)                

                if len(errors) != 0:
                    context["errors"] = errors
            
                if len(query_response_imagefilepaths) != 0:
                    
                    context["image_filepaths"] = query_response_imagefilepaths
       
        return render(request, 'index.html', context)
    
##################################################################################################################################
# Calculates Wednesday based on Friday date
def get_wed_date(fri_date):
    fri_date = datetime.strptime(fri_date, '%Y-%m-%d')
    wed_date = fri_date + \
                timedelta(days = -2)
    
    print("Inside get_wed_date func",wed_date.date())
    print("type of wed_date",type(wed_date.date()))
    return wed_date.date()

<<<<<<< HEAD
##################################################################################################################################
# Converts the Friday Date from %Y-%m-%d to Month Date, Year
def get_fri_textdate(fri_date,lang):
=======
# Converts the Date from %Y-%m-%d to Month Date, Year
def textdate(date,lang):
>>>>>>> main

    date = datetime.strptime(date, '%Y-%m-%d')
    
    if lang == "fr":
        fr_date_text = date.strftime("%b %d, %Y")
        print("Inside textdate fr_date_text",fr_date_text)
        return fr_date_text
       
    else:
        en_date_text = date.strftime("%d %B, %Y")
        print("Inside textdate en_date_text",en_date_text)
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