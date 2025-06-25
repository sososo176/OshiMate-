from django import template

register = template.Library()

@register.filter
def get_dynamic_image(item, index):
    return getattr(item, f'image{index}', None)
