wagtail-daterange
========================

django-admin-rangefilter app, add the filter by a custom date / datetime range on the admin UI.

Requirements
------------

* Python 2.7+ or Python 3.3+
* Django 1.8+


Installation
------------

Use your favorite Python package manager to install the app from PyPI, e.g.

Example:

``pip install git+git://<this repo>``


Add ``wagtail_daterange`` to ``INSTALLED_APPS``:

Example:

.. code:: python

    INSTALLED_APPS = (
        ...
        'wagtail_daterange',
        ...
    )


Example usage
-------------

In admin
~~~~~~~~

.. code:: python

    from django.contrib import admin
    from wagtail_daterange.filter import DateRangeFilter, DateTimeRangeFilter

    @admin.register(Post)
    class PostAdmin(admin.ModelAdmin):
        list_filter = (
            ('created_at', DateRangeFilter), ('updated_at', DateTimeRangeFilter),
        )
