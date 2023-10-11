from django import forms
from datetime import datetime
from functools import partial
from django.utils.translation import gettext, gettext_lazy as _

PROVINCE_CHOICES= [
    ('AB', _('Alberta')),
    ('BC', _('British Columbia')),
    ('MB', _('Manitoba')),
    ('NB', _('New Brunswick')),
    ('NL',_('Newfoundland and Labrador')),
    ('NS',_('Nova Scotia')),
    ('ON',_('Ontario')),
    ('PE',_('Prince Edward Island')),
    ('QC',_('Quebec')),
    ('SK',_('Saskatchewan'))
    ]

THEME_CHOICES = [
    ('COL',_('Collaboration')),
    ('GOV',_('Governance')), 
    ('CHA',_('Challenges')),
    ('FUN',_('Funding')),
    ('POL',_('Policy')),
    ('EDI',_('EDI')),
    ('OTH',_('Other'))
    
]

LANGUAGE_CHOICES = [
    ('EN',_('English')),
    ('FR',_('French'))
]

ORGANIZATION_SIZES = [('SM',_('Small')),
('MD',_('Medium')),
('LG',_('Large'))]

AGE = [
    ('OLD',_('Registered before 1990')),
    ('NEW',_('Registered after 1990')),
]

EXPENDITURE = [
    ('XS',_('Extra Small (Less than $150,000)')),
    ('SM',_('Small (Less than $400,000)' )), 
    ('MD',_('Medium (Between $400,000-$850,000)')),
    ('LG',_('Large (More than $850,000)')),
    ('XL',_('Extra Large (More than $2,000,000)')),
    # ('XXL',_('Super Large (More than $55,800,000)')),
]

REGION = [
    ('West Coast',_('West Coast')),
    ('Prairie Provinces',_('Prarie Provinces')),
    ('Central Canada',_('Central Canada')),
    ('Atlantic Region',_('Atlantic Region')),
    ('North',_('North Canada')),
]

SUBSAMPLE = [
    ('SS1',_('Foundations')),
    ('SS2',_('Volunteer-run charities')),
    ('SS3',_('Charities in BC')),
    ('SS4',_('Geographic regions')),
    ('SS5',_('Charities in QC')),
    ('SS6',_('International charities')),
]


HUMANRESOURCES = [
    ('PD',_('Paid Employees')),
    ('VOL',_('Only Volunteer Run'))
]

DateInput = partial(forms.DateInput, {'class': 'dateinput','autocomplete':'off'})

class ProvinceFilterForm(forms.Form):
    province= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=PROVINCE_CHOICES,
                                        label=_('Province'),required=False)

class LanguageFilterForm(forms.Form):
    language = forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=LANGUAGE_CHOICES,
                                        label=_('Participant Language Preference'),required=False)

class OrgsizeFilterForm(forms.Form):
    size = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=ORGANIZATION_SIZES,
                                    label=_('Size'),required=False)
    
class AgeFilterForm(forms.Form):
    age = forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=AGE,
                                        label=_('Age'),required=False)
    
class ExpenditureFilterForm(forms.Form):
    expenditure = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=EXPENDITURE,
                                        label=_('Expenditure'),required=False)

class SubsampleFilterForm(forms.Form):
    subsample = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=SUBSAMPLE,
                                        label=_('Subsample'),required=False)
    
class HumanResourcesFilterForm(forms.Form):
    humanresources = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),                choices=HUMANRESOURCES,label=_('Human Resources'),required=False)

class RegionFilterForm(forms.Form):
    region = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),choices=REGION,label=_('Region'),required=False)



# New Changes for a different theme    
class ThemeFilterForm(forms.Form):
    theme= forms.MultipleChoiceField(widget=forms.RadioSelect(),choices=THEME_CHOICES,label='',
                                    required=False)


class DateFilterForm(forms.Form):
    report_date = forms.DateField(widget=DateInput(),label='',required=False)
