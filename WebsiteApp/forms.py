from django import forms

PROVINCE_CHOICES= [
    ('Alberta', 'Alberta'),
    ('British Columbia', 'British Columbia'),
    (' Manitoba', ' Manitoba'),
    ('New Brunswick', 'New Brunswick'),
    ('Newfoundland and Labrador','Newfoundland and Labrador'),
    ('Nova Scotia','Nova Scotia'),
    ('Ontario','Ontario'),
    ('Prince Edward Island','Prince Edward Island'),
    ('Quebec','Quebec'),
    ('Saskatchewan','Saskatchewan')
    ]

class ProvinceForm(forms.Form):
    province= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=PROVINCE_CHOICES,)


THEME_CHOICES = [
    ('FUN','Funding'),
    ('GOV','Governance'),
    ('POL','Policy'),
    ('COL','Collaboration'),
    ('CHA','Challenges'),
    ('EDI','EDI'),
    ('OTH','Other')
]

class ThemeForm(forms.Form):
    theme= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=THEME_CHOICES,)


LANGUAGE_CHOICES = [
    ('ENGLISH','English'),
    ('FRENCH','French')
]

class LanguageForm(forms.Form):
    language = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=LANGUAGE_CHOICES,)

class DateInput(forms.DateInput):
    input_type = 'date'

class SearchDateForm(forms.Form):
    weekly_date_field = forms.DateField(widget = DateInput(format="%Y-%m-%d"),input_formats=["%Y-%m-%d"],label='Report Date/Date du compte rendu')