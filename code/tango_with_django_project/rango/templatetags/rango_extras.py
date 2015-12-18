# This templatetag is no longer used
from rango.models import Category
from django import template

register = template.Library()

def get_category_list(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}


