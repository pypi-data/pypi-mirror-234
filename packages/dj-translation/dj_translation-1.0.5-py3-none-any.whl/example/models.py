from django.db import models
from django.utils.timezone import now

from dj_translation.models import TranslationField, TranslatedValue


class TranslatableModel(models.Model):
    title = TranslationField(blank=True, null=True, default=dict, rich_text=False)
    description = TranslationField(blank=True, null=True, default=dict, rich_text=True)
    created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return TranslatedValue(self.title).translate()
