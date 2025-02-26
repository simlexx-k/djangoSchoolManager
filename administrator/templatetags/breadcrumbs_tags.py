from django import template

register = template.Library()

@register.inclusion_tag('admin/breadcrumbs.html')
def render_breadcrumbs(breadcrumbs):
    return {'breadcrumbs': breadcrumbs}
