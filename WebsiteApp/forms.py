from django import forms

PROVINCE_CHOICES= [
    ('AB', 'Alberta'),
    ('BC', 'British Columbia'),
    ('MB', ' Manitoba'),
    ('NB', 'New Brunswick'),
    ('NL','Newfoundland and Labrador'),
    ('NS','Nova Scotia'),
    ('ON','Ontario'),
    ('PE','Prince Edward Island'),
    ('QC','Quebec'),
    ('SK','Saskatchewan')
    ]

THEME_CHOICES = [
    ('FUN','Funding'),
    ('GOV','Governance'),
    ('POL','Policy'),
    ('COL','Collaboration'),
    ('CHA','Challenges'),
    ('EDI','EDI'),
    ('OTH','Other')
]

LANGUAGE_CHOICES = [
    ('EN','English'),
    ('FR','French')
]

ORGANIZATION_SIZES = [('SMALL','Small'),
('MEDIUM','Medium'),
('LARGE','Large')]

# FIELD_OF_WORK = []

from django import forms
from django.forms.widgets import SelectDateWidget
from datetime import datetime, timedelta

from django.forms.widgets import MultiWidget, Select

class WeekSelectorWidget(MultiWidget):
    def __init__(self, attrs=None):
        year_choices = [(year, year) for year in range(2022, 2030)] # set range of year choices
        week_choices = [(week, week) for week in range(1, 53)] # set range of week choices
        widgets = [
            Select(choices=year_choices),
            Select(choices=week_choices),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.year, value.isocalendar()[1]]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        year = int(data.get(name + '_0'))
        week = int(data.get(name + '_1'))
        return datetime.date.fromisocalendar(year, week, 1)




class FilterForm(forms.Form):
    year_week = forms.DateField(widget=WeekSelectorWidget)
    province= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=PROVINCE_CHOICES,)
    theme= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=THEME_CHOICES,)
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=LANGUAGE_CHOICES,)
    size = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=ORGANIZATION_SIZES,)
    
    
