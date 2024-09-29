from django import template
from administrator.utils import get_grade as utils_get_grade

register = template.Library()

@register.filter
def grade_from_score(score):
    try:
        return utils_get_grade(float(score))
    except ValueError:
        return "N/A"

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
