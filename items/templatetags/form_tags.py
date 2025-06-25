# items/templatetags/form_tags.py
from django import template

register = template.Library()

@register.simple_tag
def get_dynamic_form_field(form, field_name):
    return form[field_name]
