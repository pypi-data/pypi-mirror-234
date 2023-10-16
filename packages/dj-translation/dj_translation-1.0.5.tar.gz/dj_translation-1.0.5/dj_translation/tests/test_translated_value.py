from typing import Iterable

from django.test import TestCase, override_settings
from django.utils.translation import activate, get_language, deactivate
from dj_translation.models import TranslatedValue

import os
from django.conf import settings


class TranslatedValueStructureTestCase(TestCase):
    def setUp(self) -> None:
        self.translated_value = TranslatedValue({})

    def test_it_has___init___method(self):
        self.assertTrue(hasattr(self.translated_value, '__init__'))

    def test_it_has___str___method(self):
        self.assertTrue(hasattr(self.translated_value, '__str__'))

    def test_it_get_method(self):
        self.assertTrue(hasattr(self.translated_value, 'get'))

    def tset_it_has___getitem___method(self):
        self.assertTrue(hasattr(self.translated_value, '__getitem__'))

    def test_it_has___eq___method(self):
        self.assertTrue(hasattr(self.translated_value, '__eq__'))

    def test_it_has___ne___method(self):
        self.assertTrue(hasattr(self.translated_value, '__ne__'))

    def test_it_has___bool___method(self):
        self.assertTrue(hasattr(self.translated_value, '__bool__'))

    def test_it_has___len___method(self):
        self.assertTrue(hasattr(self.translated_value, '__len__'))

    def test_it_has___iter___method(self):
        self.assertTrue(hasattr(self.translated_value, '__iter__'))

    def test_it_has___repr___method(self):
        self.assertTrue(hasattr(self.translated_value, '__repr__'))

    def test_it_has_items_method(self):
        self.assertTrue(hasattr(self.translated_value, 'items'))

    def test_it_has_values_method(self):
        self.assertTrue(hasattr(self.translated_value, 'values'))

    def test_it_has_keys_method(self):
        self.assertTrue(hasattr(self.translated_value, 'keys'))

    def test_it_has_translate_method(self):
        self.assertTrue(hasattr(self.translated_value, 'translate'))


class TranslatedValueInitMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.translations = {'ar': 'arabic', 'en': 'english'}
        self.translated_value = TranslatedValue(self.translations)

    def test_it_set_translations_value(self):
        self.assertEqual(self.translated_value.translations, self.translations)

    def test_it_raises_validation_error_when_translations_value_is_not_dict(self):
        with self.assertRaises(ValueError):
            TranslatedValue('invalid value')

    def test_validation_error_message(self):
        with self.assertRaisesMessage(
                ValueError, 'Invalid value for translations attribute expecting dict'
        ):
            TranslatedValue('invalid value')


class TranslatedValueStrMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.translations = {'ar': 'arabic', 'en': 'english'}
        self.translated_value = TranslatedValue(self.translations)

    def test_it_returns_string_value(self):
        self.assertIsInstance(self.translated_value.__str__(), str)

    def test_it_return_translated_string_based_on_current_locale(self):
        self.assertEqual(self.translated_value.__str__(), self.translations[get_language()])


class TranslatedValueGetMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def tearDown(self) -> None:
        deactivate()

    def test_it_returns_empty_str_when_value_is_none(self):
        translated_value = TranslatedValue(None)
        self.assertEqual(translated_value.get(), "")

    @override_settings(LANGUAGE_CODE='en-us')
    def test_it_returns_translation_with_provided_langauge(self):
        translation = self.translated_value.get('ar')
        self.assertEqual(translation, 'arabic')

    @override_settings(LANGUAGE_CODE='en-us')
    def test_it_returns_translation_with_current_locale_when_provided_language_not_exist_in_translations(self):
        translation = self.translated_value.get('invalid')
        self.assertEqual(translation, 'english')

    @override_settings(LANGUAGE_CODE='en-us')
    def test_it_return_translation_with_current_locale_when_not_providing_language_value(self):
        translation = self.translated_value.get()
        self.assertEqual(translation, 'english')

    @override_settings(LANGUAGE_CODE='af')
    def test_it_returns_translation_with_first_locale_when_current_locale_and_provided_language_does_not_exist_in_translations(
            self):
        translation = self.translated_value.get('fr')
        self.assertEqual(translation, 'arabic')

    def test_it_returns_empty_str_if_translations_is_empty(self):
        translated_value = TranslatedValue({})
        translation = translated_value.get()
        self.assertEqual(translation, "")

    @override_settings(LANGUAGE_CODE='en-us')
    def test_it_returns_translation_with_current_locale_when_change_locale(self):
        activate('ar')
        self.assertEqual(self.translated_value.get(), 'arabic')


class TranslatedValueGetItemMethodTestCase(TestCase):
    @override_settings(LANGUAGE_CODE='en-us')
    def test_it_returns_translation_with_provided_language(self):
        value = {'ar': 'arabic', 'en-us': 'english'}
        translated_value = TranslatedValue(value)
        self.assertEqual(translated_value.__getitem__('ar'), 'arabic')


class TranslatedValueEqMethodTestCase(TestCase):
    def test_it_returns_true_when_compare_with_equivalent_translated_value(self):
        value = {'ar': 'arabic', 'en-us': 'english'}
        translated_value_1 = TranslatedValue(value)
        translated_value_2 = TranslatedValue(value)
        self.assertTrue(translated_value_1.__eq__(translated_value_2))

    def test_it_return_false_when_compare_to_unequal_translated_value(self):
        value_1 = {'ar': 'arabic1', 'en-us': 'english1'}
        value_2 = {'ar': 'arabic2', 'en-us': 'english2'}
        translated_value_1 = TranslatedValue(value_1)
        translated_value_2 = TranslatedValue(value_2)
        self.assertFalse(translated_value_1.__eq__(translated_value_2))


class TranslatedValueNeMethodTestCase(TestCase):
    def test_it_returns_false_when_compare_with_equivalent_translated_value(self):
        value = {'ar': 'arabic', 'en-us': 'english'}
        translated_value_1 = TranslatedValue(value)
        translated_value_2 = TranslatedValue(value)
        self.assertFalse(translated_value_1.__ne__(translated_value_2))

    def test_it_return_true_when_compare_to_unequal_translated_value(self):
        value_1 = {'ar': 'arabic1', 'en-us': 'english1'}
        value_2 = {'ar': 'arabic2', 'en-us': 'english2'}
        translated_value_1 = TranslatedValue(value_1)
        translated_value_2 = TranslatedValue(value_2)
        self.assertTrue(translated_value_1.__ne__(translated_value_2))


class TranslatedValueBoolMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_returns_bool_value(self):
        self.assertIsInstance(self.translated_value.__bool__(), bool)

    def test_it_returns_false_if_translations_is_none(self):
        translated_value = TranslatedValue(None)
        self.assertFalse(translated_value.__bool__())

    def test_it_returns_true_when_translations_has_value(self):
        self.assertTrue(self.translated_value.__bool__())

    def test_it_returns_false_when_translations_is_empty_dict(self):
        self.assertFalse(TranslatedValue({}).__bool__())


class TranslatedValueIterMethodTestCase(TestCase):
    def test_it_returns_iterable_type(self):
        translated_value = TranslatedValue({'ar': 'arabic', 'en-us': 'english'})
        self.assertIsInstance(translated_value.__iter__(), Iterable)


class TranslatedValueReprMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_return_TranslatedValue_representation(self):
        value = self.translated_value.__repr__()
        self.assertEqual(value, "<class TranslatedValue>")

    def test_it_returns_str_value(self):
        self.assertIsInstance(self.translated_value.__repr__(), str)


class TranslatedValueItemsMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_returns_items_of_translations_value(self):
        self.assertEqual(self.translated_value.items(), self.value.items())

    def test_when_dict_is_empty(self):
        translated_value = TranslatedValue({})
        self.assertEqual(translated_value.items(), {}.items())


class TranslatedValueValuesMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_returns_values_of_translations_dict(self):
        self.assertEqual(list(self.translated_value.values()), list(self.value.values()))


class TranslatedValueKeysMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_returns_keys_of_translations_dict(self):
        self.assertEqual(list(self.translated_value.keys()), list(self.value.keys()))


class TranslatedValueTranslateMethodTestCase(TestCase):
    def setUp(self) -> None:
        self.value = {'ar': 'arabic', 'en-us': 'english'}
        self.translated_value = TranslatedValue(self.value)

    def test_it_returns_calls_get_method(self):
        self.assertEqual(self.translated_value.translate(), self.translated_value.get())
        self.assertEqual(self.translated_value.translate('ar'), self.translated_value.get('ar'))
