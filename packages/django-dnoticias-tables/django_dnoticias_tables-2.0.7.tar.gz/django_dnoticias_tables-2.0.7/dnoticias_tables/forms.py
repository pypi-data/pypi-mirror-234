from typing import Any, Optional, Iterable

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms.fields import Field, FileField
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django import forms


class GenericForm(forms.Form):
    def get_field_class(
        self,
        field_type: str,
        label: str,
        field_initial: Optional[Any] = None,
        queryset: Optional[Iterable[Any]] = None,
    ) -> Field:
        return {
            "choices": forms.ChoiceField(
                label=label,
                choices=field_initial or [],
                required=False,
                widget=forms.SelectMultiple(attrs={"data-max-options": "1"}),
            ),
            "multiple_choices": forms.MultipleChoiceField(
                label=label,
                choices=field_initial or [],
                required=False,
                widget=forms.SelectMultiple,
            ),
            "model_multiple_choices": forms.ModelMultipleChoiceField(
                label=label,
                queryset=queryset or ContentType.objects.none(),
                required=False,
                widget=forms.SelectMultiple,
            ),
            "model_choices": forms.ModelChoiceField(
                label=label,
                queryset=ContentType.objects.none(),
                required=False
            ),
            "text": forms.CharField(label=label, max_length=256, required=False),
            "date": forms.CharField(
                label=label,
                required=False,
                max_length=128,
                widget=forms.TextInput(attrs={"class": "form-control datepicker"})
            ),
            "daterange": forms.CharField(
                label=label,
                required=False,
                max_length=128,
                widget=forms.TextInput(attrs={"class": "form-control daterange"})
            ),
        }.get(field_type, None)

    def __init__(self, *args, **kwargs):
        self.field_data = kwargs.pop("fields")
        super().__init__(*args, **kwargs)

        for field, data in self.field_data.items():
            self.fields[field] = self.get_field_class(
                data["type"],
                data["label"],
                data["initial"],
                data["queryset"]
            )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def get_filters(self):
        filters = Q()

        for field, data in self.field_data.items():
            value = self.cleaned_data.get(field)
            field_type = data["type"]
            queryset_filter_by = data["queryset_filter_by"]

            if value:
                if queryset_filter_by:
                    from .datatable import FilterType

                    if queryset_filter_by in [FilterType.ISNULL, ]:
                        value = bool(int(value))

                    filters &= Q(**{f"{field}__{queryset_filter_by}": value})

                elif field_type == "model_choices":
                    filters &= Q(**{f"{field}__id": value.id})
                elif field_type == "model_multiple_choices":
                    filters &= Q(**{f"{field}__id__in": value})
                elif field_type == "choices":
                    filters &= Q(**{f"{field}": value})
                elif field_type == "multiple_choices":
                    filters &= Q(**{f"{field}__in": value})
                elif field_type == "date":
                    filters &= Q(**{f"{field}__date": value})
                elif field_type == "daterange":
                    min_date, max_date = value.split(" até ")
                    filters &= (
                        Q(**{f"{field}__gte": min_date})
                        & Q(**{f"{field}__lte": max_date})
                    )
                else:
                    filters &= Q(**{field: value})

        return filters
