from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def is_active(request, url_name):
    if resolve(request.path_info).url_name == url_name:
        return 'bg-gray-900 text-white'
    return 'text-gray-300 hover:bg-gray-700 hover:text-white'
