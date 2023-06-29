from django import forms
from datetime import datetime
from functools import partial
from django.utils.translation import gettext, gettext_lazy as _
# from django_select2.forms import Select2MultipleWidget,Select2Widget

PROVINCE_CHOICES= [
    ('AB', _('Alberta')),
    ('BC', _('British Columbia')),
    ('MB', _(' Manitoba')),
    ('NB', _('New Brunswick')),
    ('NL',_('Newfoundland and Labrador')),
    ('NS',_('Nova Scotia')),
    ('ON',_('Ontario')),
    ('PE',_('Prince Edward Island')),
    ('QC',_('Quebec')),
    ('SK',_('Saskatchewan'))
    ]

THEME_CHOICES = [
    ('FUN',_('Funding')),
    ('GOV',_('Governance')),
    ('POL',_('Policy')),
    ('COL',_('Collaboration')),
    ('CHA',_('Challenges')),
    ('EDI',_('EDI')),
    ('OTH',_('Other'))
]

LANGUAGE_CHOICES = [
    ('EN',_('English')),
    ('FR',_('French'))
]

ORGANIZATION_SIZES = [('SMALL',_('Small')),
('MEDIUM',_('Medium')),
('LARGE',_('Large'))]

AGE = [
    ('OLD',_('Old (Registered before 1990)')),
    ('NEW',_('New (Registered after 1990)'))
]

# FIELD_OF_WORK = []

DateInput = partial(forms.DateInput, {'class': 'dateinput'})

    
class ProvinceFilterForm(forms.Form):
    province= forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=PROVINCE_CHOICES,
                                        label=_('Province'),required=False)

class LanguageFilterForm(forms.Form):
    language = forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=LANGUAGE_CHOICES,
                                        label = _('Language Preference'),required=False)

class OrgsizeFilterForm(forms.Form):
    size = forms.MultipleChoiceField(widget=forms.SelectMultiple(),choices=ORGANIZATION_SIZES,
                                    label=_('Size'),required=False)
    
class AgeFilterForm(forms.Form):
    age = forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=AGE,
                                        label = _('Age'),required=False)


 # New Changes for a different theme    
class ThemeFilterForm(forms.Form):
    theme= forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=THEME_CHOICES,
                                    label = _('Theme'),required=False)
    
class DateFilterForm(forms.Form):
    report_date = forms.DateField(widget=DateInput(),label=_('Report Date'),required=False)
