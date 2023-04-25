from django.shortcuts import render
from .forms import FilterForm
from scripts.Utils import FrontEndQuery
from scripts.Controller import HandleFrontEndQuery
from django.utils.translation import gettext,get_language
from datetime import datetime, timedelta

# Create your views here.
def report_results_EN(request):

    

    if request.GET:
        form_filter = FilterForm(request.GET)
       
        context = {'form_filter' : form_filter}

        date = request.GET.get('report_date', None)
        if date is None:
            date = str(datetime.now().date())
        else:
            date = (request.GET['report_date'])
        location = (request.GET.getlist('province'))
        question_theme = (request.GET.getlist('theme'))
        # language_preference = request.GET.getlist('language')
        language_preference = get_language()
        organization_size = (request.GET.getlist('size'))

        print(context)

        if date == "2022-12-23" or date == "2022-12-30" :
            info = gettext(" 🥳🥳🥳 HAPPY HOLIDAYS  NO REPORT PUBLISHED DURING THIS WEEK 🥳🥳🥳")
            context['info'] = info

        else:
            
            wednesday_date = get_wed_date(date,lang=get_language())
            friday_text_date = get_fri_textdate(date,lang=get_language())

            context['wednesday_date'] = wednesday_date
            context['friday_text_date'] = friday_text_date

            front_end_query = FrontEndQuery()

            front_end_query.date = date
            front_end_query.locations = location
            front_end_query.questionThemes = question_theme
            front_end_query.languagePreference = language_preference
            front_end_query.organizationSizes = organization_size
            front_end_query.qualtricsSurveyID = ''
            
            if front_end_query:
                query_response_imagefilepaths,query_response_csv,errors = HandleFrontEndQuery(front_end_query)
                print(query_response_imagefilepaths)

                if len(errors) != 0:
                    context["errors"] = errors
            
                if len(query_response_imagefilepaths) != 0:
                    context["image_filepaths"] = query_response_imagefilepaths


        return render(request, 'index.html', context)

    else:
        form_filter = FilterForm()
        friday_date = str(get_fridaydate_from_todays_date(datetime.now()))
        friday_text_date = get_fri_textdate(friday_date,lang=get_language())
        wednesday_date = get_wed_date(friday_date,lang=get_language())
        context = {'form_filter' : form_filter,'friday_text_date' : friday_text_date,'wednesday_date' : wednesday_date}
        front_end_query = FrontEndQuery()
        front_end_query.date = str(get_fridaydate_from_todays_date(datetime.now()))
      
        if front_end_query:
                query_response_imagefilepaths,query_response_csv,errors = HandleFrontEndQuery(front_end_query)
                print(query_response_imagefilepaths)
                

                if len(errors) != 0:
                    context["errors"] = errors
            
                if len(query_response_imagefilepaths) != 0:
                    
                    context["image_filepaths"] = query_response_imagefilepaths
       
        return render(request, 'index.html', context)
    

# Calculates Wednesday based on Friday date
def get_wed_date(fri_date,lang):
    fri_date = datetime.strptime(fri_date, '%Y-%m-%d')
    wednesday = fri_date + \
                timedelta(days = -2)
    if lang == "fr":
        wednesday_fr = wednesday.strftime("%d %B, %Y")
        wednesday_fr = datetime.strptime(wednesday_fr,"%d %B, %Y")
        return(wednesday_fr.date())
    else:
        print(lang)
        wednesday = wednesday.strftime("%d %B, %Y")
        
        return(wednesday)

# Converts the Friday Date from %Y-%m-%d to Month Date, Year
def get_fri_textdate(fri_date,lang):

    fri_date = datetime.strptime(fri_date, '%Y-%m-%d')
    
    if lang == "fr":
        friday_fr = fri_date.strftime("%b %d, %Y")
        friday_fr = datetime.strptime(friday_fr, "%b %d, %Y")
        return (friday_fr.date())
    else:
        friday = fri_date.strftime("%d %B, %Y")
        return friday


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