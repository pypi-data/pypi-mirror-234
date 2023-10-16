from django.contrib import admin
from .models import TranslatableModel
from .forms import TranslatableForm


class CustomModelAdmin(admin.ModelAdmin):
    form = TranslatableForm


admin.site.register(TranslatableModel, CustomModelAdmin)  # Register your model and admin class
