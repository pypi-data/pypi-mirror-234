import logging
import math

from django.db.models import Model, QuerySet
from django.http import JsonResponse
from django.core import serializers

from .utils import get_model_attr
from .process import Process


logger = logging.getLogger(__name__)


class MetronicProcess(Process):
    def __init__(self, request):
        super().__init__(request)
        logger.debug(request.POST)
        self.extra_thead = self.get_extra_thead()
        self.length = int(request.POST.get('pagination[perpage]', 10))
        self.start = (int(request.POST.get('pagination[page]', 0)) - 1) * self.length
        self.order_column = self.get_order_column_index(request)
        self.order_direction = '-' if request.POST.get('sort[sort]', 'asc') == 'desc' else ''
        self.table_id = self.get_table_id()
        self.table_search_id = self.get_table_search_id()
        self.global_search = request.POST.get('query[{}]'.format(self.table_search_id), '')

    def get_table_id(self):
        return ""

    def get_table_search_id(self):
        return "{}_search".format(self.get_table_id())

    def get_extra_thead(self):
        return []

    def get_order_column(self):
        return self.orderable_fields[self.order_column]

    def get_order_column_index(self, request):
        default_field_index = self.get_default_order_field_index()
        order_field_requested = request.POST.get(
            'sort[field]', self.orderable_fields[default_field_index])
        for index, field in enumerate(self.orderable_fields):
            if field.startswith(order_field_requested):
                return index
        return default_field_index

    def pre_config(self):
        self.order_attr = self.orderable_fields[self.order_column]
        self.is_reverse = True if self.order_direction == '-' else False

    def get_default_order_field_index(self):
        return 0

    def get_custom_method_signature(self, field):
        return "get_custom_{}_value".format(field)

    def resolve_best_value(self, instance, field):
        custom_function = getattr(self, self.get_custom_method_signature(field), None)
        if custom_function:
            return custom_function(instance)
        else:
            value = get_model_attr(instance, field, default=None)

            is_queryset = isinstance(value, QuerySet)
            is_model = isinstance(value, Model)
            if is_queryset or is_model:
                if is_model:
                    elements = [value]
                else:
                    elements = value
                value = serializers.serialize("json", elements)
            else:
                value = super().resolve_best_value(instance, field)
            return value

    def get_ajax_objects(self):
        context = dict()
        context["meta"] = self.get_meta()
        context["data"] = self.get_data()
        return JsonResponse(data=context, safe=False)

    def get_meta(self):
        return {
            "page": math.floor(int(self.start/self.length) + 1),
            "pages": self.paginator.num_pages,
            "perpage": self.length,
            "total": self.length * self.paginator.num_pages,
            "sort": self.get_sort(),
            "field": self.get_order_column()
        }

    def get_data(self):
        context = []
        for index, instance in enumerate(self.object_list):
            json_order = vars(self.serialized_object_list[index])
            for field in self.extra_thead:
                json_order[field[0]] = self.resolve_best_value(
                    self.object_list[index], field[0]
                )
            context.append(json_order)
        return context
