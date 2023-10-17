from __future__ import annotations
from typing import Any, Iterable, Optional, Type
from dataclasses import dataclass
from datetime import datetime

from django.db.models.fields.files import FieldFile
from django.views.generic import View
from django.db.models import Model
from django.utils import timezone

from .choices import FilterType


@dataclass
class BaseColumn:
    name: Optional[str] = None
    searchable: Optional[bool] = True
    search_type: Optional[str] = FilterType.ICONTAINS
    visible: Optional[bool] = True
    auto_hide: Optional[bool] = True
    orderable: Optional[bool] = True
    datetime_format: Optional[str] = "%d/%m/%Y %H:%M"
    width: Optional[int] = 100
    align: Optional[str] = "left"
    url_name: Optional[str] = None
    url_arg: Optional[str] = "pk"

    _creation_counter = 0

    def get_value(self, field: str, obj: Type[Model], view: Optional[Type[View]]):
        """Get the value for a given field

        :param field: The field to get the value for
        :param obj: The object to get the value for
        :param view: The view that is rendering the table
        :return: The value for the field
        :rtype: Any
        :raises: AttributeError if the field does not exist
        :raises: NotImplementedError if the attr is not implemented
        """
        raise NotImplementedError()


class Column(BaseColumn):
    def get_value(self, field: str, obj: Type[Model], view: Optional[Type[View]]) -> Any:
        """Get the value for a given field

        :param field: The field to get the value for
        :param obj: The object to get the value for
        :param view: The view that is rendering the table
        :return: The value for the field
        :rtype: Any
        """
        value = getattr(obj, field)

        if type(value) == datetime:
            try:
                value = timezone.localtime(value).strftime(self.datetime_format)
            except ValueError:
                value = value.strftime(self.datetime_format)
        elif isinstance(value, FieldFile):
            value = value.url if value else None

        return value


class ColumnMethod(BaseColumn):
    def __init__(self, method: Optional[str] = None, **kwargs):
        """Create a new ColumnMethod

        :param method: The method to use to get the value for the field
        :type method: Optional[str]
        """
        self.method = method
        super().__init__(**kwargs)

    def get_method_name(self, field: str) -> str:
        """Get the default method name for a given field if the user did not specify one

        :param field: The field to get the method name for
        :return: The method name for the field
        :rtype: str
        """
        return self.method or f"get_{field}"

    def get_value(self, field: str, obj: Type[Model], view: Optional[Type[View]]) -> Any:
        """Get the value for a given field

        :param field: The field to get the value for"""
        value = getattr(view, self.get_method_name(field))(obj)

        if type(value) == datetime:
            value = value.strftime(self.datetime_format)

        return value


class ColumnChoice(BaseColumn):
    def __init__(self, choices: Optional[Iterable[tuple]] = None, **kwargs):
        self.choices = choices
        super().__init__(**kwargs)

    def get_choice_label(self, value: str) -> str:
        """Get the label for a given choice value

        :param value: The value to get the label for
        :return: The label for the choice value
        :rtype: str
        """
        return next((choice[1] for choice in self.choices if choice[0] == value))

    def get_value(self, field: str, obj: Type[Model], view: Optional[Type[View]]):
        value = getattr(obj, field)
        return value


@dataclass
class ColumnModel(BaseColumn):
    def __init__(
        self,
        attributes: Optional[list[str]] = None,
        lookup_fields: Optional[list[str]] = None,
        url_attribute: Optional[str] = "pk",
        **kwargs
    ):
        """Create a new ColumnModel

        :param attributes: The attributes to get from the model
        :param lookup_fields: The lookup fields used in search filters
        :param url_attribute: The attribute to use to get the url for the model
        """
        self.attributes = attributes
        self.url_attribute = url_attribute
        self.lookup_fields = lookup_fields
        super().__init__(**kwargs)

    def get_value(self, field: str, obj: Type[Model], view: Optional[Type[View]]) -> Any:
        """Get the value for a given field

        :param field: The field to get the value for
        :param obj: The object to get the value for
        :param view: The view that is rendering the table
        :return: The value for the field
        :rtype: Any
        """
        model = getattr(obj, field)
        value = dict()

        for attribute in self.attributes:
            try:
                attr_value = getattr(model, attribute)
            except AttributeError:
                continue

            if type(attr_value) == datetime:
                attr_value = attr_value.strftime(self.datetime_format)

            value.update({attribute: attr_value})

        return value
