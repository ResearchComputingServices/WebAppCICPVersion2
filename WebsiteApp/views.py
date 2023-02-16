from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchDateForm,ProvinceForm,ThemeForm,LanguageForm

# Create your views here.
def report_results_EN(request):
    form_searchdate = SearchDateForm()
    form_province = ProvinceForm()
    form_theme = ThemeForm()
    form_lang = LanguageForm()
    context = {'form_searchdate' : form_searchdate,'form_province':form_province,'form_theme':form_theme,'form_lang':form_lang }
    return render(request, 'index.html', context)