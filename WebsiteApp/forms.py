from django import forms
from datetime import datetime
from functools import partial
from django.utils.translation import gettext, gettext_lazy as _

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

# FIELD_OF_WORK = []

DateInput = partial(forms.DateInput, {'class': 'dateinput'})


class PrimaryFilterForm(forms.Form):
    report_date = forms.DateField(widget=DateInput(),label=_('Report Date'),required=False)
    theme= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=THEME_CHOICES,
                                    label = _('Theme'),required=False)
    
    
class ProvinceFilterForm(forms.Form):
    province= forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=PROVINCE_CHOICES,
                                        label=_('Province'),required=False)

class LanguageFilterForm(forms.Form):
    language = forms.MultipleChoiceField(widget=forms.SelectMultiple(choices=LANGUAGE_CHOICES),
                                        label = _('Language Preference'),required=False)

class OrgsizeFilterForm(forms.Form):
    size = forms.MultipleChoiceField(widget=forms.SelectMultiple(choices=ORGANIZATION_SIZES),
                                    label=_('Size'),required=False)
    
