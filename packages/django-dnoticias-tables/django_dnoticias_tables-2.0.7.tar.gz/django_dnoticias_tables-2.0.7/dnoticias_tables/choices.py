import django
from django.db import models


# Check if django version is 3.2 or higher
version = django.get_version()


class FilterType:
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    EXACT = "exact"
    IEXACT = "iexact"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    ISNULL = "isnull"
    STARTSWITH = "startswith"
    ISTARTSWITH = "istartswith"
    ENDSWITH = "endswith"
    IENDSWITH = "iendswith"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"
    WEEK_DAY = "week_day"
    TIME = "time"
    DATE = "date"
    BLANK = "blank"

if version >= "3.2":
    class YesNoChoices(models.IntegerChoices):
        NO = 0, "Não"
        YES = 1, "Sim"


    class ActiveChoices(models.IntegerChoices):
        INACTIVE = 0, "Inativo"
        ACTIVE = 1, "Ativo"
