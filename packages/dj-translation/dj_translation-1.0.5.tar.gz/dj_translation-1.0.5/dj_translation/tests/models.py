from django.db import models
from django.utils.timezone import now

from dj_translation.models import TranslationField


# Translatable Model
class TranslatableTestModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = TranslationField(blank=True, null=True, default=dict, rich_text=False)
    description = TranslationField(blank=True, null=True, default=dict, rich_text=True)
    created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
