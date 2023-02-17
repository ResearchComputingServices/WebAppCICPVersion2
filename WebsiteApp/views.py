from django.shortcuts import render
from django.http import HttpResponse
# from .forms import SearchDateForm,ProvinceForm,ThemeForm,LanguageForm
from .forms import FilterForm
from scripts.Utils import FrontEndQuery
from scripts.Controller import HandleFrontEndQuery

# Create your views here.
def report_results_EN(request):
    form_filter = FilterForm()
    context = {'form_filter' : form_filter}

    location = (request.GET.getlist('province'))
    question_theme = (request.GET.getlist('theme'))
    language_preference = (request.GET.getlist('language'))
    organization_size = (request.GET.getlist('size'))

    front_end_query = FrontEndQuery()

    front_end_query.locations = location
    front_end_query.questionThemes = question_theme
    front_end_query.languagePreference = language_preference
    front_end_query.organizationSizes = organization_size

    query_response_imagefilepaths,query_response_csv = HandleFrontEndQuery(front_end_query)
    print(query_response_imagefilepaths)
    print(query_response_csv)

    return render(request, 'index.html', context)

