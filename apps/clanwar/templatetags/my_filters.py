# my_filters.py
# Some custom filters for dictionary lookup.
from django.template.defaultfilters import register

@register.filter(name='lookup')

def lookup(dic, index):
    try:
        return dic[index]
    except:
        return ''
