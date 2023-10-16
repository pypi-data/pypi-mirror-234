import inspect
import json
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets
from django.test import TestCase, override_settings
from django.utils.translation import activate, get_language

from dj_translation.models import TranslationField, TranslatedValue
from dj_translation.forms import TranslationField as TranslationFormField
from dj_translation.tests.models import TranslatableTestModel
from django.db.models import JSONField
from django.db import models


class TranslatedFieldTestCase(TestCase):

    def test_it_returns_value_correctly(self):
        my_model = TranslatableTestModel.objects.create(
            title={'en': 'English title', 'fr': 'Titre français'},
        )
        my_model_db = TranslatableTestModel.objects.get(pk=my_model.pk)
        self.assertEqual(my_model_db.title.get('en'), 'English title')
        self.assertEqual(my_model_db.title.get('fr'), 'Titre français')

    def test_it_returns_dict_from_save_method(self):
        my_model = TranslatableTestModel(
            title={'en': 'English title', 'fr': 'Titre français'},
        )
        my_model.save()
        self.assertIsInstance(my_model.title, dict)


class TranslationFieldStructureTestCase(TestCase):
    def setUp(self) -> None:
        self.translation_field = TranslationField({})

    def test_it_extends_json_field(self):
        self.assertIsInstance(self.translation_field, JSONField)

    def test_it_has_validate_method(self):
        self.assertTrue(hasattr(self.translation_field, 'validate'))

    def test_validate_method_signature(self):
        sig = inspect.signature(self.translation_field.validate)
        params = list(sig.parameters.keys())
        self.assertEquals(len(params), 2)
        self.assertIn('value', params)
        self.assertIn('model_instance', params)

    def test_it_has_formfield_method(self):
        self.assertTrue(hasattr(self.translation_field, 'formfield'))

    def test_formfield_method_signature(self):
        sig = inspect.signature(self.translation_field.formfield)
        params = list(sig.parameters.keys())
        self.assertEquals(len(params), 1)
        self.assertIn('kwargs', params)


class ValidateMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.field = TranslationField()
        self.model_instance = TranslatableTestModel()

    def test_it_calls_super_method(self):
        value = "invalid_value"
        model_instance = None
        with patch.object(models.JSONField, "validate") as mock_super:
            with self.assertRaises(ValidationError):
                self.field.validate(value, model_instance)
            mock_super.assert_called_once_with(value, model_instance)

    def test_it_raises_validation_error_when_value_is_not_dict(self):
        with self.assertRaises(ValidationError):
            self.field.validate("invalid_value", self.model_instance)

    def test_validation_error_message_when_value_is_not_dict(self):
        expected_error_message = """The provided value type is invalid. The value must be a dictionary. Please ensure that you are passing a dictionary as the value."""
        with self.assertRaisesMessage(ValidationError, expected_error_message):
            self.field.validate("invalid_value", self.model_instance)

    def test_it_raises_validation_error_when_provide_invalid_language_code(self):
        value = "invalid_value"
        model_instance = None
        with patch.object(models.JSONField, "validate") as mock_super:
            with self.assertRaises(ValidationError):
                self.field.validate(value, model_instance)

    def test_it_raises_validation_error_when_provide_language_that_is_not_exist_in_settings(self):
        with self.assertRaises(ValidationError):
            self.field.validate({'none': ''}, self.model_instance)

    def test_validation_message_when_provide_language_that_is_not_exist_in_settings(self):
        data = {'none': ''}
        with self.assertRaisesMessage(ValidationError,
                                      """The provided language key, '{}', is invalid. Please ensure that the key is properly defined and provided in the settings.""".format(
                                          'none')):
            self.field.validate(data, self.model_instance)

    def test_it_passes_when_data_is_correct(self):
        data = {'ar': ''}
        try:
            self.field.validate(data, self.model_instance)
        except Exception as e:
            self.fail(f"The method raised an exception: {e}")


class FormFieldMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.field = TranslationField()

    def test_formfield_returns_instance_of_field(self):
        form = self.field.formfield()
        self.assertIsInstance(form, forms.Field)

    def test_formfield_returns_translation_form_field_by_default(self):
        form = self.field.formfield()
        self.assertIsInstance(form, TranslationFormField)

    def test_formfield_can_override_default_form_class(self):
        formfield = self.field.formfield(form_class=TranslationFormField)
        self.assertIsInstance(formfield, TranslationFormField)
        self.assertIs(formfield.__class__, TranslationFormField)
