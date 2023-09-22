from django import template
from django.utils.translation import gettext

register = template.Library()

def template_trans(text):
    try:
        return gettext(text)
    except Exception as e:
        return text
    

register.filter('template_trans',template_trans)