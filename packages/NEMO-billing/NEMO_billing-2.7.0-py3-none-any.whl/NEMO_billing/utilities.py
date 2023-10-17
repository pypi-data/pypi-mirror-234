import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.forms import BaseForm, HiddenInput


class Months(models.IntegerChoices):
    JAN = 1, "JANUARY"
    FEB = 2, "FEBRUARY"
    MAR = 3, "MARCH"
    APR = 4, "APRIL"
    MAY = 5, "MAY"
    JUN = 6, "JUNE"
    JUL = 7, "JULY"
    AUG = 8, "AUGUST"
    SEP = 9, "SEPTEMBER"
    OCT = 10, "OCTOBER"
    NOV = 11, "NOVEMBER"
    DEC = 12, "DECEMBER"


class IntMultipleChoiceField(forms.MultipleChoiceField):
    def prepare_value(self, value):
        if value is None:
            return value
        if type(value) is list:
            return [int(val) for val in value]
        return value.split(",")

    def to_python(self, value):
        value = super().to_python(value)
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages["invalid_list"], code="invalid_list")
        return ",".join([str(val) for val in value])

    def validate(self, value):
        """Validate that the input is a list or tuple."""
        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")
        # Validate that each value in the value list is in self.choices.
        for val in value.split(","):
            if not self.valid_value(val):
                raise ValidationError(
                    self.error_messages["invalid_choice"],
                    code="invalid_choice",
                    params={"value": val},
                )


def disable_form_field(form: BaseForm, field_name):
    if field_name in form.fields:
        form.fields[field_name].disabled = True
        form.fields[field_name].required = False


def hide_form_field(form: BaseForm, field_name):
    if field_name in form.fields:
        disable_form_field(form, field_name)
        form.fields[field_name].widget = HiddenInput()


# Utility functions to compare dates that are stored in month/year format
def filter_date_year_month_gte(field_name: str, date_to_compare: datetime.date) -> Q:
    return Q(**{f"{field_name}_year__gt": date_to_compare.year}) | Q(**{f"{field_name}_year": date_to_compare.year, f"{field_name}_month__gte": date_to_compare.month})


def filter_date_year_month_gt(field_name: str, date_to_compare: datetime.date) -> Q:
    return Q(**{f"{field_name}_year__gt": date_to_compare.year}) | Q(**{f"{field_name}_year": date_to_compare.year, f"{field_name}_month__gt": date_to_compare.month})


def filter_date_year_month_lt(field_name: str, date_to_compare: datetime.date) -> Q:
    return Q(**{f"{field_name}_year__lt": date_to_compare.year}) | Q(**{f"{field_name}_year": date_to_compare.year, f"{field_name}_month__lt": date_to_compare.month})


def filter_date_year_month_lte(field_name: str, date_to_compare: datetime.date) -> Q:
    return Q(**{f"{field_name}_year__lt": date_to_compare.year}) | Q(**{f"{field_name}_year": date_to_compare.year, f"{field_name}_month__lte": date_to_compare.month})


def number_of_months_between_dates(end_date, start_date):
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
