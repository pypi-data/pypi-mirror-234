import json

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


class TranslationWidget(forms.Widget):
    template_name = 'dj_translation/dj_translation_field.html'

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.rich_text = self.attrs.get('rich_text', False)

    def render(self, name, value, attrs=None, renderer=None):
        # Convert the value to a JSON string for rendering
        if isinstance(value, dict):
            value = str(json.dumps(value))

        attrs = dict(attrs)

        if self.rich_text:
            attrs['ckeditor_config'] = json.dumps(
                getattr(settings, 'DJ_TRANSLATION_CKEDITOR_CONFIG', {
                    'toolbar': {
                        'items': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', '|', 'undo',
                                  'redo']
                    }
                }))
        attrs['rich_text'] = self.rich_text
        # Render the custom template

        context = {
            'name': name,
            'value': value,
            'rich_text': self.rich_text,
            'attrs': attrs,
        }

        return self._render(self.template_name, context, renderer)

    @property
    def media(self):
        return forms.Media(
            js=(
                "https://cdn.ckeditor.com/ckeditor5/29.2.0/classic/ckeditor.js",
                'dj_translation/js/utils.js',
                'dj_translation/js/event.js',
                'dj_translation/js/input.js',
                'dj_translation/js/display.js',
                'dj_translation/js/tabs.js',
                'dj_translation/js/translation_widget.js',
            ),
            css={
                'all': ('dj_translation/css/style.css',),
            }
        )


class TranslationField(forms.JSONField):
    def __init__(self, rich_text=False, *args, **kwargs):
        self.rich_text = rich_text
        super().__init__(*args, **kwargs)

        self.widget = TranslationWidget(attrs=self.widget.attrs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({'rich_text': self.rich_text})
        return attrs

