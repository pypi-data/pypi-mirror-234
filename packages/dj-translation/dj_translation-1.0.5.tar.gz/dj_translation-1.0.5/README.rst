==============
DJ-Translation
==============

Description
------------
The Translation Package is a Django package that simplifies the handling of translations in your Django projects. It provides a convenient way to store translation values as JSON and includes a model field, form field, and widget to facilitate translation management.

.. image:: ./docs/translation_field.png
   :width: 100%
   :align: center
   :alt: DJ-Translation Logo

Contents
---------
- `Features <#features>`_
- `Installation <#installation>`_
- `Configuration <#configuration>`_
- `Usage <#usage>`_
- `Additional Functionality <#additional-functionality>`_
- `Using DJ-Translation in the Django Admin <#using-dj-translation-in-the-django-admin>`_
- `API Reference <#api-reference>`_
- `Contributing <#contributing>`_

Features
--------
- JSON-based Translation Storage: JSON-based Translation Storage: The package allows you to store translation values as JSON, making it easy to manage and update translations.
- Model Field: It includes a custom model field that seamlessly integrates with your Django models, allowing you to store and retrieve translations effortlessly.
- Ability to handle translations for multiple languages out of the box.
- Support for rich text translation with optional CKEditor 5 integration.
- Customizable CKEditor 5 configuration for tailored editing experience.


Installation
-------------
Before installing DJ-Translation, please ensure you have Django 4.x installed. You can install DJ-Translation using pip, as follows:

.. code-block::

    $ pip install dj-translation

If you prefer to install from source, you can clone the repository from GitHub and install it manually:

.. code-block::

    $ git clone https://github.com/fritill-team/django-translation.git
    $ cd dj-translation
    $ python setup.py install

Note: It is recommended to create a virtual environment before installing DJ-Translation to keep your Django projects isolated.

Configuration
===============

Once DJ-Translation is installed, you need to add it to your Django project's settings. Open your project's ``settings.py`` file and add ``'dj_translation'`` to the ``INSTALLED_APPS`` setting:

.. code-block::

    INSTALLED_APPS = [
        # Other apps...
        'dj_translation',
    ]

Finally, run the database migrations to create the necessary tables for DJ-Translation:

.. code-block::

    python manage.py migrate


Once DJ-Translation is installed, you need to add it to your Django project's settings. Open your project's ``settings.py`` file and make the following additions:

Add the following language-related settings:

.. code-block::

    LANGUAGE_CODE = 'en-us'

    ARABIC_LANGUAGE_CODE = 'ar'
    ENGLISH_LANGUAGE_CODE = 'en'
    SPANISH_LANGUAGE_CODE = 'es'

    # Languages we provide translations for, out of the box.
    LANGUAGES = [
        (ARABIC_LANGUAGE_CODE, gettext_noop('Arabic')),
        (ENGLISH_LANGUAGE_CODE, gettext_noop('English')),
        (SPANISH_LANGUAGE_CODE, gettext_noop('Español'))
    ]

    # Languages using BiDi (right-to-left) layout
    LANGUAGES_BIDI = ["he", "ar", "ar-dz", "fa", "ur"]

Note: Adjust the language codes and names according to your specific requirements.

Add the CKEditor configuration for DJ-Translation (optional):

.. code-block::

    DJ_TRANSLATION_CKEDITOR_CONFIG = {
        'toolbar': {
            'items': ['heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', '|', 'undo', 'redo']
        }
    }

Note: The CKEditor configuration is optional and can be used to customize the CKEditor toolbar items according to your needs.



Usage
------

To utilize the translation capabilities provided by DJ-Translation, follow these guidelines:

1. Define Models: Declare a model field of type ``TranslatedField`` in your Django models to store translated values. You can use the additional attribute ``rich_text=True`` to enable CKEditor integration for the field:

.. code-block::

    from dj_translation.fields import TranslatedField

    class YourModel(models.Model):
        translated_field = TranslatedField(rich_text=True)

2. Forms Integration: Use the ``TranslatedFormField`` in your Django forms to enable translation input and display. If you have a translated field with CKEditor enabled, make sure to include CKEditor assets in your form template:

.. code-block::

    {% extends "base.html" %}

    {% block content %}
        <form method="post">
            {% csrf_token %}
            {{ form.media }}
            {{ form.translated_field }}
            <button type="submit">Save</button>
        </form>
    {% endblock %}

3. Widget Customization: Customize the appearance and behavior of the ``TranslatedWidget`` to match your application's requirements.

4. Retrieving Translations: Retrieve translated values from the ``TranslatedField`` and display them in your templates or API responses.


Additional Functionality
=========================

``TranslatedValue Class``
~~~~~~~~~~~~~~~~~~~~~~~~
The `TranslatedValue` class is provided by DJ-Translation to work with translated values. You can pass the value returned from the `TranslatedField` to create a `TranslatedValue` instance.

``Translate Function``
~~~~~~~~~~~~~~~~~~

The `TranslatedValue` class provides a `translate` function that can be used to retrieve the translated value based on the activated language or a specific language.

Example usage:

.. code-block::

    # Create a TranslatedValue instance
    translated_value = TranslatedValue(value_from_field)

    # Retrieve the translated value for the activated language
    activated_language_translation = translated_value.translate()

    # Retrieve the translated value for a specific language
    specific_language_translation = translated_value.translate(language='fr')

``Using DJ-Translation in the Django Admin``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DJ-Translation can be seamlessly integrated into the Django admin interface to manage translations. To enable DJ-Translation in the admin, follow these steps:

1. Create your model and use `TranslationField`

.. code-block::

    class TranslatableModel(models.Model):
        title = TranslationField(blank=True, null=True, default=dict, rich_text=False)
        description = TranslationField(blank=True, null=True, default=dict, rich_text=True)
        created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
        updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

        def __str__(self):
            return TranslatedValue(self.title).translate()


2. Register your models with translated fields in the admin site by creating an admin.py file in your app directory (if not already created) and define a custom ModelAdmin class:

.. code-block::

    class CustomModelAdmin(admin.ModelAdmin):
        form = TranslatableForm


    admin.site.register(TranslatableModel, CustomModelAdmin)  # Register your model and admin class


3. Now, when you access the admin interface for your models, the translated fields will be available for input and display.


API Reference
==============

The package provides the following API elements:

``TranslatedField``
~~~~~~~~~~~~~~~~~~

A model field that handles the storage and retrieval of translated values.

``TranslatedFormField``
~~~~~~~~~~~~~~~~~~~~~~

A form field for translation input.

``TranslatedWidget``
~~~~~~~~~~~~~~~~~~~~

A widget for displaying translations.

Contributing
=============

We welcome contributions to DJ-Translation! If you would like to contribute code, report issues, or submit pull requests, please refer to our guidelines at [link to contribution guidelines].


