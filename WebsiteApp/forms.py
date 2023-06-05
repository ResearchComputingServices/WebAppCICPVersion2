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

# FIELD_OF_WORK = []

DateInput = partial(forms.DateInput, {'class': 'dateinput'})


class PrimaryFilterForm(forms.Form):
    report_date = forms.DateField(widget=DateInput(),label=_('Report Date'),required=False)
    theme= forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=THEME_CHOICES,
                                    label = _('Theme'),required=False)



class MultiSelectWidget(forms.SelectMultiple):
    class Media:
        css = {
            'all': ('https://code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css',),
        }
        js = (
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://code.jquery.com/ui/1.12.1/jquery-ui.js',
        )

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['class'] = 'multiselect-widget'
        return attrs
    
class ProvinceFilterForm(forms.Form):
    province= forms.MultipleChoiceField(widget=MultiSelectWidget,choices=PROVINCE_CHOICES,
                                        label=_('Province'),required=False)

class LanguageFilterForm(forms.Form):
    language = forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=LANGUAGE_CHOICES,
                                        label = _('Language Preference'),required=False)

class OrgsizeFilterForm(forms.Form):
    size = forms.MultipleChoiceField(widget=forms.SelectMultiple,choices=ORGANIZATION_SIZES,
                                    label=_('Size'),required=False)
    
