import ast
import json

from django import template
from django.conf import settings
from django.conf.locale import LANG_INFO

from dj_translation.models import TranslatedValue

register = template.Library()


@register.filter
def value_to_json(translation):
    return json.dumps(ast.literal_eval(translation))


@register.simple_tag
def languages_data():
    language_list = []
    for language_code, language_name in settings.LANGUAGES:
        language_info = {
            'code': str(language_code),
            'name': str(language_name),
            'bidi': LANG_INFO.get(language_code, {}).get('bidi', False),
            'name_local': LANG_INFO.get(language_code, {}).get('name_local')
        }
        language_list.append(language_info)

    return json.dumps(language_list, ensure_ascii=False)


@register.filter
def translate(translations, language=None):
    return TranslatedValue(translations).translate(language)

