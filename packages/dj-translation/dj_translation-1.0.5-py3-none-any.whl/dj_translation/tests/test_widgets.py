import json
from itertools import chain

from django import forms
from django.forms import TextInput, Textarea
from django.test import TestCase
from django.utils.safestring import mark_safe

from dj_translation.models import TranslatedValue
from dj_translation.forms import TranslationWidget


class TranslationWidgetTest(TestCase):
    def setUp(self):
        self.widget = TranslationWidget()

    def test_it_adds_rich_text_flag_to_class(self):
        widget = TranslationWidget(attrs={'rich_text': True})
        self.assertTrue(hasattr(widget, 'rich_text'))

    def test_rich_text_value(self):
        widget = TranslationWidget(attrs={'rich_text': True})
        self.assertTrue(getattr(widget, 'rich_text'))
        widget = TranslationWidget(attrs={'rich_text': False})
        self.assertFalse(getattr(widget, 'rich_text'))

    def test_template_name(self):
        self.assertEqual(self.widget.template_name, 'dj_translation/dj_translation_field.html')

