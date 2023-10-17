from typing import Any, Iterable, Optional, Callable
from dataclasses import dataclass


@dataclass
class CustomAction:
    name: str
    icon: str
    url_name: str
    arg_name: Optional[str] = "pk"
    method: Optional[str] = "GET"
    target: Optional[str] = "_self"
    permission: Optional[str] = None
    show_function: Optional[Callable[[Any], bool]] = None


@dataclass
class Filter:
    CHOICES = "choices"
    MULTIPLE_CHOICES = "multiple_choices"
    MODEL_CHOICES = "model_choices"
    MODEL_MULTIPLE_CHOICES = "model_multiple_choices"
    DATERANGE = "daterange"
    DATE = "date"

    label: str
    type: str
    initial: Optional[Iterable[tuple]] = None
    placeholder: Optional[str] = None
    queryset_filter_by: Optional[str] = None
    queryset: Optional[Iterable] = None
