import inspect

from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
from django.core.paginator import Paginator


class CustomPaginator(Paginator):
    @cached_property
    def count(self):
        """Return the total number of objects, across all pages. This function has
        been modified to return a count of primary keys instead a count using every
        field (unnecesary).

        Performance improvement: 12.134s to 0.008s
        """
        c = getattr(self.object_list, 'count', None)

        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return self.object_list.values("pk").count()

        return len(self.object_list)
