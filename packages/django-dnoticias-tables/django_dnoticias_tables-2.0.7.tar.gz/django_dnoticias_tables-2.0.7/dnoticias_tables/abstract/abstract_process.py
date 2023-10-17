import logging
from abc import abstractmethod, ABC

from django.urls import reverse

from .order_object import OrderObject

logger = logging.getLogger(__name__)


class AbstractProcess(ABC):

    def __init__(self, request):
        self.request = request
        self.draw = int(request.GET.get('draw', 0))
        self.length = int(request.GET.get('length', 10))
        self.start = int(request.GET.get('start', 0))
        self.order_column = int(request.GET.get('order[0][column]', '1'))
        self.order_direction = '-' if request.GET.get(
            'order[0][dir]', 'asc') == 'desc' else ''
        self.global_search = request.GET.get('search[value]', '')
        self.object_list = []
        self.thead = []
        self.on_click_url = "#"
        self.extra_params = {}
        self.queryset = []
        self.searchable_fields = []
        self.id_prefix = ""
        self.is_orderable = False
        self.thead = self.set_thead()
        self.orderable_fields = self.set_orderable_fields()
        self.searchable_fields = self.set_searchable()
        self.paginator = None
        logger.debug("Requesting data to a table\n"
                    "Process: {}\n"
                    "Length: {}\n"
                    "Start: {}\n"
                    "Ordered by: {}\n"
                    "Ordered in: {}\n"
                    "Pesquisar por:{}\n".format(self.get_view_details(), self.length, self.start, self.order_column,
                                                self.order_direction, self.global_search))

    def get_sort(self):
        return self.request.GET.get('order[0][dir]', 'asc')

    def get_order_column(self):
        return self.thead[self.order_column]

    @abstractmethod
    def get_view_details(self):
        return ""

    def has_click_option(self):
        return self.on_click_url != "#"

    def template(self):
        self.pre_config()
        self.queryset = self.set_query_set()
        self.filtered_object_list = self.produce_query_set()
        self.object_list = self.post_config()
        self.serialized_object_list = self.to_table_topics()
        return self.get_objects()

    @abstractmethod
    def set_thead(self):
        return []

    def set_orderable_fields(self):
        return [item[0] for item in self.set_thead()]

    @abstractmethod
    def set_searchable(self):
        return []

    def pre_config(self):
        self.order_column -= 1
        self.order_attr = self.thead[self.order_column][0]
        self.is_reverse = True if self.order_direction == '-' else False

    @abstractmethod
    def produce_query_set(self):
        return []

    @abstractmethod
    def set_query_set(self):
        return []

    def to_table_topics(self):
        obj_set = []
        for item in self.object_list:
            data = dict()
            if self.request.GET.get("selectable", False):
                data["selectable"] = ""
            data["redirect_link"] = self.resolve_redirect_link(item)
            data["DT_RowId"] = self.add_row_id(item)
            for field in self.thead:
                field_name = field[0]
                try:
                    if "__" in field_name:
                        values = field_name.split("__")
                        temp = item
                        size = len(values)
                        instance = None
                        for i in range(size):
                            if i == (size - 1):
                                instance = temp
                                field = values[i]
                            else:
                                temp = getattr(temp, values[i])
                        value = self.resolve_best_value(instance, field)
                    else:
                        value = self.resolve_best_value(item, field_name)
                    data[field_name] = value
                except:
                    data[field_name] = "Error"
                    logger.exception("Error")
            obj_set.append(OrderObject(data, self.order_attr))
        return obj_set

    def resolve_best_value(self, instance, field):
        return str(getattr(instance,field, ""))

    def resolve_redirect_link(self, instance):
        if self.on_click_url != "#":
            keys = self.extra_params.keys()
            if len(keys) > 0:
                kwargs = self.extra_params.get("kwargs", None)
                args = self.extra_params.get("args", None)

                resolved_kwargs = {}
                resolved_args = ()

                for key, element in kwargs.items():
                    if "__" in element:
                        splited_attrs = element.split("__")
                        temp = instance
                        for attr in splited_attrs:
                            temp = getattr(temp, attr, None)
                        resolved_kwargs[key] = temp
                    else:
                        resolved_kwargs[key] = getattr(instance, element, None)

                if args is not None:
                    for element in args:
                        resolved_args += (getattr(instance, element, None))

                return reverse(self.on_click_url, kwargs=resolved_kwargs, args=resolved_args)
            else:
                return reverse(self.on_click_url)
        else:
            return "#"

    def add_row_id(self, item):
        return self.id_prefix + str(self.get_instance_id(item))

    @abstractmethod
    def get_instance_id(self, item):
        return None

    def get_objects(self):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.get_ajax_objects()
        else:
            return self.serialized_object_list

    def get_ajax_objects(self):
        result = []

        for instance in self.serialized_object_list:
            json_order = vars(instance)
            result.append(json_order)

        return {
            "draw": self.draw,
            "recordsTotal": self.get_total_records_total(),
            "recordsFiltered": self.get_total_filtered_records(),
            "data": result,
        }

    def get_object_list(self):
        return self.object_list

    def get_total_records_total(self):
        return 0

    def get_total_filtered_records(self):
        return 0
