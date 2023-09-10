from django import template
import pandas as pd
from django.utils.safestring import mark_safe

#https://www.geeksforgeeks.org/django-template-filters/
register = template.Library()

@register.filter(name="df_to_html")
def df_to_html(df: pd.DataFrame):
    return mark_safe( df.to_html() )

#https://stackoverflow.com/questions/5427809/django-template-object-type 
@register.filter
def classname(obj):
    return obj.__class__.__name__