from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from example.forms import TranslatableForm
from example.models import TranslatableModel


class CreateOrUpdateTranslatableView(View):
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            instance = TranslatableModel.objects.get(pk=kwargs.get('pk'))
            form = TranslatableForm(instance=instance)
        else:
            form = TranslatableForm()
        return render(request, template_name='translation.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk', None):
            instance = TranslatableModel.objects.get(pk=kwargs.get('pk'))
            form = TranslatableForm(request.POST, instance=instance)
        else:
            form = TranslatableForm(request.POST)

        if form.is_valid():
            instance = form.save()

            return redirect(reverse('example:create'))
        return render(request, template_name='translation.html', context={'form': form})


class TranslatableListView(ListView):
    model = TranslatableModel
    paginate_by = 100
    template_name = 'translation_listing.html'
