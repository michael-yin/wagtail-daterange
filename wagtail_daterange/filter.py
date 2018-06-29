# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime
import django

try:
    import pytz
except ImportError:
    pytz = None

from collections import OrderedDict

from django import forms
from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _

from wagtail.admin import widgets


class DateRangeFilter(admin.filters.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_gte = '{}__gte'.format(field_path)
        self.lookup_kwarg_lte = '{}__lte'.format(field_path)

        super(DateRangeFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.request = request
        self.form = self.get_form(request)

    def get_timezone(self, request):
        return timezone.get_default_timezone()

    @staticmethod
    def make_dt_aware(value, timezone):
        if settings.USE_TZ and pytz is not None:
            default_tz = timezone
            if value.tzinfo is not None:
                value = default_tz.normalize(value)
            else:
                value = default_tz.localize(value)
        return value

    def choices(self, cl):
        yield {
            'system_name': slugify(self.title),
            'query_string': cl.get_query_string(
                {}, remove=self._get_expected_fields()
            )
        }

    def expected_parameters(self):
        return self._get_expected_fields()

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.filter(
                    **self._make_query_filter(request, validated_data)
                )
        return queryset

    def _get_expected_fields(self):
        return [self.lookup_kwarg_gte, self.lookup_kwarg_lte]

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params['{0}__gte'.format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_gte, datetime.time.min),
                self.get_timezone(request),
            )
        if date_value_lte:
            query_params['{0}__lte'.format(self.field_path)] = self.make_dt_aware(
                datetime.datetime.combine(date_value_lte, datetime.time.max),
                self.get_timezone(request),
            )

        return query_params

    def get_template(self):
        return 'wagtail_daterange/date_filter.html'

    template = property(get_template)

    def get_form(self, request):
        form_class = self._get_form_class()
        return form_class(self.used_parameters)

    def _get_form_class(self):
        fields = self._get_form_fields()
        form_class = type(
            str('DateRangeForm'),
            (forms.BaseForm,),
            {'base_fields': fields}
        )
        return form_class

    def _get_form_fields(self):
        return OrderedDict((
                (self.lookup_kwarg_gte, forms.DateField(
                    label='',
                    widget=widgets.AdminDateInput(attrs={'placeholder': _('From date')}),
                    localize=True,
                    required=False
                )),
                (self.lookup_kwarg_lte, forms.DateField(
                    label='',
                    widget=widgets.AdminDateInput(attrs={'placeholder': _('To date')}),
                    localize=True,
                    required=False
                )),
        ))


class DateTimeRangeFilter(DateRangeFilter):

    def _get_form_fields(self):
        return OrderedDict((
                (self.lookup_kwarg_gte, forms.DateTimeField(
                    label='',
                    widget=widgets.AdminDateTimeInput(attrs={'placeholder': _('From date')}),
                    localize=True,
                    required=False
                )),
                (self.lookup_kwarg_lte, forms.DateTimeField(
                    label='',
                    widget=widgets.AdminDateTimeInput(attrs={'placeholder': _('To date')}),
                    localize=True,
                    required=False
                )),
        ))

    def _make_query_filter(self, request, validated_data):
        query_params = {}
        date_value_gte = validated_data.get(self.lookup_kwarg_gte, None)
        date_value_lte = validated_data.get(self.lookup_kwarg_lte, None)

        if date_value_gte:
            query_params['{0}__gte'.format(self.field_path)] = self.make_dt_aware(
                date_value_gte, self.get_timezone(request)
            )
        if date_value_lte:
            query_params['{0}__lte'.format(self.field_path)] = self.make_dt_aware(
                date_value_lte, self.get_timezone(request)
            )

        return query_params
