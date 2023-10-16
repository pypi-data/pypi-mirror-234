import inspect
import json

from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Textarea
from django.test import TestCase
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _

from dj_translation.models import TranslatedValue
from dj_translation.forms import TranslationField, TranslationWidget


class TranslationFormFieldClassStructureTest(TestCase):
    def setUp(self) -> None:
        self.form_field = TranslationField()

    def test_field_inherits_from_JSONField(self):
        self.assertIsInstance(self.form_field, TranslationField)
        self.assertIsInstance(self.form_field, forms.JSONField)

    def test_init_method_parameters(self):
        init_signature = inspect.signature(TranslationField.__init__)

        expected_parameters = [
            'self',
            'rich_text',
            'args',
            'kwargs',
        ]

        for parameter in expected_parameters:
            self.assertIn(parameter, init_signature.parameters)

        self.assertEqual(len(init_signature.parameters), len(expected_parameters))

    def test_field_has_widget_attrs_method(self):
        self.assertTrue(hasattr(self.form_field, 'widget_attrs'))

    def test_widget_attrs_parameters(self):
        signature = inspect.signature(TranslationField.widget_attrs)
        self.assertIn('widget', signature.parameters)


class TranslationFormFieldTestCase(TestCase):
    def setUp(self) -> None:
        self.form_field = TranslationField()

    def test_default_widget_is_textinput(self):
        self.assertIsInstance(self.form_field.widget, forms.Widget)

    def test_widget_type_is_translation_widget(self):
        self.assertIsInstance(self.form_field.widget, TranslationWidget)

    def test_that_rich_text_is_in_widget_attrs(self):
        attrs = self.form_field.widget_attrs(widget=TranslationWidget())
        self.assertIn('rich_text', attrs)

    def test_it_updates_widget_attrs_with_rich_text(self):
        form_field = TranslationField(rich_text=True)
        self.assertTrue(form_field.widget_attrs(widget=TranslationWidget())['rich_text'])
