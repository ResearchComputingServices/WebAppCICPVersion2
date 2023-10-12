from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from scripts.Utils import *
from scripts.Controller import HandleFrontEndQuery
from django.utils.translation import gettext, get_language
from datetime import datetime, timedelta
from django_tex.shortcuts import render_to_pdf
from WebAppCICPVersion2 import settings
from operator import itemgetter
from InteractiveDB.models import SurveyTable
from django.utils.translation import activate, deactivate



##################################################################################################################################
# Create your views here.


def formInitialization():
    frontEndQuery = FrontEndQuery()
    context = {}

    context["themeFilter"] = ThemeFilterForm()
    context["dateFilter"] = DateFilterForm()
    context["province_form_filter"] = ProvinceFilterForm()
    context["language_form_filter"] = LanguageFilterForm()
    # context["org_size_form_filter"] = OrgsizeFilterForm()
    context["age_form_filter"] = AgeFilterForm()
    context["expenditure_form_filter"] = ExpenditureFilterForm()
    context['region_form_filter'] = RegionFilterForm()
    context["subsample_form_filter"] = SubsampleFilterForm()
    context['human_resources_form_filter'] = HumanResourcesFilterForm()

    return context, frontEndQuery

def mapSelectedFilterChoices(selectedCodes,selectedChoices):
    filterChoiceMapping = dict(selectedChoices)
    selectedNames = [filterChoiceMapping[code] for code in selectedCodes]
    return selectedNames


def dateInitialization(latestReport, dateSearchReport):
    if latestReport:
        # Get the latest Friday date from today and Format the date from Y%-%m-%d to respective english and french formats in text
        friday_text_date = textdate(
            str(get_fridaydate_from_todays_date(datetime.now())), lang=get_language()
        )
        wednesday_text_date = textdate(
            str(get_wed_date(str(get_fridaydate_from_todays_date(datetime.now())))),
            lang=get_language(),
        )

    elif len(dateSearchReport) != 0:
        friday_text_date = textdate(str(dateSearchReport), lang=get_language())
        wednesday_text_date = textdate(
            str(get_wed_date(dateSearchReport)), lang=get_language()
        )

    return friday_text_date, wednesday_text_date


def latest_report(request):

    latestDate = str(get_wed_date(str(get_fridaydate_from_todays_date(datetime.now()))))
    context, frontEndQuery = formInitialization()
    friday_text_date, wednesday_text_date = dateInitialization(True, "")

    context["friday_text_date"] = friday_text_date
    context["wednesday_date"] = wednesday_text_date
    context["subTheme"] = getWeeklySubTheme(None,latestDate,get_language())
    context["YearandWeek"] = getYearandWeek(latestDate)

    # Pass the wednesday date to select the images from media folder
    frontEndQuery.date = latestDate
    frontEndQuery.siteLanguage = get_language()

    if frontEndQuery:
        query_response_imagefilepaths, query_response_csv, errors,= HandleFrontEndQuery(
            frontEndQuery
        )

        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:
            context["image_filepaths"] = query_response_imagefilepaths
        else:
            context["info"] = gettext(
                "NO REPORT PUBLISHED DURING THIS WEEK")

    return render(request, "index.html", context)


# Function to render two different pages for theme and date


def themeOrDate(request, theme, date):
    context, frontEndQuery = formInitialization()

    print("theme",theme)
    if date is None:
        if theme[0] == 'Funding':
            theme[0] = "FUN"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'Governance':
            theme[0] = "GOV"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'Policy':
            theme[0] = "POL"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'Collaboration':
            theme[0] = "COL"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'Challenges':
            theme[0] = "CHA"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'EDI':
            theme[0] = "EDI"
            frontEndQuery.questionThemes = theme

        elif theme[0] == 'Other':
            theme[0] = "OTH"   
            frontEndQuery.questionThemes = theme

        else:
            print("Inside Else")
            frontEndQuery.questionThemes = theme

    elif theme is None:
        frontEndQuery.date = str(get_wed_date(date))

        friday_text_date, wednesday_text_date = dateInitialization(False, date)

        context["friday_text_date"] = friday_text_date
        context["wednesday_date"] = wednesday_text_date

    # Get the choice mappings from forms file to display the filters selected and pass them to 
    # a function to get the names of the choices
    provinceChoices = ProvinceFilterForm().fields['province'].choices
    ageChoices = AgeFilterForm().fields['age'].choices
    expenditureChoices = ExpenditureFilterForm().fields['expenditure'].choices
    regionChoices = RegionFilterForm().fields['region'].choices
    subsampleChoices = SubsampleFilterForm().fields['subsample'].choices
    humanresourcesChoices = HumanResourcesFilterForm().fields['humanresources'].choices

    # Get the selected filters as a list and pass them to frontEndQuery object
    frontEndQuery.locations = request.GET.getlist("province")
    frontEndQuery.age = request.GET.getlist("age")
    frontEndQuery.expenditure = request.GET.getlist("expenditure")
    frontEndQuery.region = request.GET.getlist("region")
    frontEndQuery.subsample = request.GET.getlist("subsample")
    frontEndQuery.humanresources = request.GET.getlist("humanresources")
    # frontEndQuery.languagePreference = context["languagePreference"] = request.GET.getlist("language")

    # Pass the selected filters along with their choice mappings to the context so that they are displayed like the options on the sidebar
    context["locations"] =  mapSelectedFilterChoices(request.GET.getlist("province"),provinceChoices)
    context["age"] = mapSelectedFilterChoices(request.GET.getlist("age"),ageChoices)
    context["expenditure"] = mapSelectedFilterChoices(request.GET.getlist("expenditure"),expenditureChoices)
    context["region"] = mapSelectedFilterChoices(request.GET.getlist("region"),regionChoices)
    context["subsample"] = mapSelectedFilterChoices(request.GET.getlist("subsample"),subsampleChoices)
    context["humanresources"] = mapSelectedFilterChoices(request.GET.getlist("humanresources"),humanresourcesChoices)


    frontEndQuery.qualtricsSurveyID = ""
    frontEndQuery.siteLanguage = get_language()

    if frontEndQuery:
        query_response_imagefilepaths, query_response_csv, errors,= HandleFrontEndQuery(
            frontEndQuery
        )

    return query_response_imagefilepaths, query_response_csv, errors, context


def landingPageView(request):
    context, frontEndQuery = formInitialization()

    questionTheme = request.GET.getlist("theme")
    reportDate = request.GET.get("report_date")

    if len(questionTheme) != 0:
        (
            query_response_imagefilepaths,
            query_response_csv,
            errors,
            context,
        ) = themeOrDate(request, theme=questionTheme, date=None)


        subfolder_data = []

        for image_path in query_response_imagefilepaths:
            subfolder, filename = os.path.split(image_path)
            subfolder = os.path.basename(subfolder)

            if subfolder == 'tmpImages':
                subfolder,filename = filename.split('Q')
                
            found = False
            for item in subfolder_data:
                if len(subfolder) == 4:
                    subfolder = subfolder.replace("W","W0")
                if item['name'] == subfolder:
                    item['images'].append(image_path)
                    found = True
                    break
            
            
            if not found:
                subfolderFullName = subfolder.replace("Y",gettext("Year-")).replace("W",gettext("Week-"))
                subfolder_data.append({
                    'name': subfolder, 
                    'images': [image_path],
                    'fullname':subfolderFullName,
                    'subtheme':getWeeklySubTheme(subfolder,None,get_language())
                    })
                
        sorted_subfolder_data = sorted(subfolder_data, key=itemgetter('name')) 

        context["filtered"] = "filteredReport"

        if questionTheme[0] == "FUN":
            context["questionTheme"] = gettext("Funding")

        if questionTheme[0] == "GOV":
            context["questionTheme"] = gettext("Governance")

        if questionTheme[0] == "POL":
            context["questionTheme"] = gettext("Policy")

        if questionTheme[0] == "COL":
            context["questionTheme"] = gettext("Collaboration")

        if questionTheme[0] == "CHA":
            context["questionTheme"] = gettext("Challenges")

        if questionTheme[0] == "EDI":
            context["questionTheme"] = gettext("EDI")

        if questionTheme[0] == "OTH":
            context["questionTheme"] = gettext("Other")

        if len(errors) != 0:
            context["errors"] = errors

        if len(query_response_imagefilepaths) != 0:
            context["image_filepaths"] = sorted_subfolder_data
            print(context["image_filepaths"])

            # Create a dat file to print the report
            content_dict = {}
            for i, filepath in enumerate(query_response_imagefilepaths, 1):
                key = f"Figure{i}"
                content_dict[key] = settings.BASE_ROOT + filepath
            content_dict['theme'] = context["questionTheme"]

        

            datfilepath = settings.BASE_DIR / "WebsiteApp/templates/latexgraphics.dat"
            try:
                with open(datfilepath, "w") as f:
                    for key in content_dict.keys():
                        f.write(f"{key},{content_dict[key]}\n")
            except FileNotFoundError:
                print("Dat file not found")


        return render(request, "index.html", context)

    elif reportDate:

        noSurveyDates = ["2022-12-23","2022-12-30","2023-07-28","2023-08-04"]
        if reportDate in noSurveyDates:
            info = gettext(
                "NO REPORT PUBLISHED DURING THIS WEEK"
            )
            context["info"] = info

            return render(request, "index.html", context)

        else:
            (
                query_response_imagefilepaths,
                query_response_csv,
                errors,
                context,
            ) = themeOrDate(request, None, reportDate)

            friday_text_date, wednesday_text_date = dateInitialization(
                False, reportDate
            )

            context["filtered"] = "filteredReport"
            context["friday_text_date"] = friday_text_date
            context["wednesday_date"] = wednesday_text_date
            context["reportDate"] = reportDate
            context["subTheme"] = getWeeklySubTheme(None,str(get_wed_date(reportDate)),get_language())
            context["YearandWeek"] = getYearandWeek(str(get_wed_date(reportDate)))
           

            if len(errors) != 0:
                context["errors"] = errors

            if len(query_response_imagefilepaths) != 0:
                context["image_filepaths"] = query_response_imagefilepaths

            # Create a dat file to print the report
            content_dict = {}
            for i, filepath in enumerate(query_response_imagefilepaths, 1):
                key = f"Figure{i}"
                content_dict[key] = settings.BASE_ROOT + filepath
            content_dict['date'] = context["reportDate"]

            datfilepath = settings.BASE_DIR / "WebsiteApp/templates/latexgraphics.dat"

            try:
                print(content_dict)
                with open(datfilepath, "w") as f:
                    for key in content_dict.keys():
                        f.write(f"{key},{content_dict[key]}\n")
            except FileNotFoundError:
                print("Dat file not found")

            return render(request, "index.html", context)

    else:
        if reportDate == None and len(questionTheme) == 0:
            return render(request, "lpage.html", context)


def printReport(request):
    template_name = "main.tex"
    context = {}
    # Call render_to_pdf function and capture the output
    pdf_output = render_to_pdf(
        request, template_name, context, filename="my_report.pdf"
    )
    return pdf_output


##################################################################################################################################
# Calculates Wednesday based on Friday date
def get_wed_date(fri_date):
    fri_date = datetime.strptime(fri_date, "%Y-%m-%d")
    wed_date = fri_date + timedelta(days=-2)
    return wed_date.date()


# Converts the Date from %Y-%m-%d to Month Date, Year
def textdate(date, lang):
    date = datetime.strptime(date, "%Y-%m-%d")

    if lang == "fr":
        fr_date_text = date.strftime("%d %B, %Y")
        return fr_date_text

    else:
        en_date_text = date.strftime("%d %B, %Y")

        return en_date_text


##################################################################################################################################
# Fetching the Friday date based on user input date
def get_fridaydate_from_todays_date(todays_date):
    # Using current time
    week_day = todays_date.weekday()

    # Monday
    if week_day == 0:
        # Prev Friday
        past_week_friday = todays_date + timedelta(days=-3)
        return past_week_friday.date()

    # Tuesday
    elif week_day == 1:
        # Prev Friday
        past_week_friday = todays_date + timedelta(days=-4)
        return past_week_friday.date()

    # Wednesday
    elif week_day == 2:
        # Prev Friday
        past_week_friday = todays_date + timedelta(days=-5)
        return past_week_friday.date()

    # Thursday
    elif week_day == 3:
        # Prev Friday
        past_week_friday = todays_date + timedelta(days=-6)
        return past_week_friday.date()

    # Friday
    elif week_day == 4:
        # Today - Friday
        this_week_friday = todays_date + timedelta(days=0)
        return this_week_friday.date()

    # Saturday
    elif week_day == 5:
        # Present Week Friday
        this_week_friday = todays_date + timedelta(days=-1)
        return this_week_friday.date()

    # Sunday
    elif week_day == 6:
        # Present Week Friday
        this_week_friday = todays_date + timedelta(days=-2)
        return this_week_friday.date()


def getWeeklySubTheme(surveyWeek,releaseDate,language):
    try:
        if surveyWeek:
            if language == 'fr':
                subTheme = SurveyTable.objects.filter(surveyWeek=surveyWeek).values('surveysubThemeFrench')
                subtheme = subTheme[0]['surveysubThemeFrench']
            else:
                subTheme= SurveyTable.objects.filter(surveyWeek=surveyWeek).values('surveysubThemeEnglish')
                subtheme = subTheme[0]['surveysubThemeEnglish']


        elif releaseDate:

            if language == 'fr':
                subTheme = SurveyTable.objects.filter(releaseDate=releaseDate).values('surveysubThemeFrench')
                subtheme = subTheme[0]['surveysubThemeFrench']
            else:
                subTheme = SurveyTable.objects.filter(releaseDate=releaseDate).values('surveysubThemeEnglish')
                subtheme = subTheme[0]['surveysubThemeEnglish']        

        return subtheme
    except Exception as e:
        # Handle any exceptions here and return an error message
        error_message = gettext("Unavailable")
        return error_message

def getYearandWeek(releaseDate):
    try:
        surveyWeek = SurveyTable.objects.filter(releaseDate=releaseDate).values('surveyWeek')
        surveyWeek = surveyWeek[0]['surveyWeek']
        surveyWeek = surveyWeek.replace("Y",gettext("Year-")).replace("W",gettext("Week-"))
        return surveyWeek
    except Exception as e:
        # Handle any exceptions here and return an error message
        error_message = gettext("Report not yet generated for this date.")
        return error_message