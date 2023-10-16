import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from .forms import TranslationField as TranslationFormField


class TranslationField(models.JSONField):

    def __init__(self, *args, **kwargs):
        self.rich_text = kwargs.pop('rich_text', False)
        super().__init__(*args, **kwargs)

    # def from_db_value(self, value, expression, connection):
    #     if value is None:
    #         return None
    #     try:
    #         value_dict = json.loads(value)
    #     except ValueError:
    #         raise ValidationError(_("Invalid JSON string for TranslationField"))
    #
    #     return TranslatedValue(value_dict)

    def formfield(self, **kwargs):
        defaults = {"form_class": TranslationFormField, "rich_text": self.rich_text}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    # def to_python(self, value):
    #     if isinstance(value, TranslatedValue):
    #         return value.translations
    #     elif isinstance(value, dict):
    #         return value
    #     elif value is None:
    #         return None
    #
    #     else:
    #         raise ValidationError(
    #             _("Invalid value type for TranslationField")
    #         )

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if isinstance(value, dict):
            for lang, text in value.items():
                if lang not in dict(settings.LANGUAGES).keys():
                    raise ValidationError(
                        _("The provided language key, '%(lang)s', is invalid. Please ensure that the key is properly defined and provided in the settings."),
                        params={"lang": lang},
                    )
        else:
            raise ValidationError(
                _("""The provided value type is invalid. The value must be a dictionary. Please ensure that you are passing a dictionary as the value."""))

    # def get_db_prep_save(self, value, connection):
    #     if value is None:
    #         return None
    #
    #     if isinstance(value, TranslatedValue):
    #         value = value.translations
    #
    #     if not isinstance(value, TranslatedValue) and not isinstance(value, dict):
    #         raise ValidationError(_('Invalid value type for TranslationField'))
    #     return super().get_db_prep_save(value, connection)


class TranslatedValue:
    def __init__(self, translations):
        if not isinstance(translations, dict) and translations is not None:
            raise ValueError(_('Invalid value for translations attribute expecting dict'))
        self.translations = translations

    def __str__(self):
        return str(self.get())

    def get(self, language=None):
        """
        Returns the value of the field for the specified locale, or the value for the locale specified
        in Django settings, or any available value.

        Parameters:
        language: (optional) The locale for the desired translation. Defaults to None.

        Returns:
        The translated text from the JSON field for the specified locale, or None if the locale is not found.
        """

        if not self.translations:
            return ""

        # First, try to return the value for the specified locale
        if language and language in self.keys():
            return self.translations.get(language, "")

        # Next, try to return the value for the current locale
        current_locale = get_language()
        if current_locale and current_locale in self.keys():
            return self.translations.get(current_locale, "")

        # Finally, return the first available value
        for v in self.values():
            if v:
                return v

        return ""

    def __getitem__(self, language):
        return self.translations.get(language, "")

    def __eq__(self, other):
        if isinstance(other, TranslatedValue):
            return self.translations == other.translations
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return bool(self.translations)

    def __len__(self):
        return len(self.translations)

    def __iter__(self):
        return iter(self.translations)

    def __repr__(self):
        return f"<class {type(self).__name__}>"

    def items(self):
        return self.translations.items()

    def values(self):
        return self.translations.values()

    def keys(self):
        return self.translations.keys()

    def translate(self, language=None):
        """
        Returns the value of the field for the specified locale, or the value for the locale specified
        in Django settings, or any available value.

        Parameters:
            language: (optional) The locale for the desired translation. Defaults to None.

        Returns:
            The translated text from the JSON field for the specified locale, or None if the locale is not found.
        """
        return self.get(language)
