# portfolio_app/core/templatetags/custom_filters.py
from django import template
import re

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Разделяет строку по разделителю"""
    if not value:
        return []
    return [item.strip() for item in value.split(delimiter)]

@register.filter
def strip(value):
    """Убирает пробелы с обеих сторон"""
    return value.strip()

@register.filter
def get_item(dictionary, key):
    """Получает элемент из словаря по ключу"""
    return dictionary.get(key)

