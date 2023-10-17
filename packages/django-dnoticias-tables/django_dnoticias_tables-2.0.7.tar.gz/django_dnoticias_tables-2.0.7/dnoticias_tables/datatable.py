from typing import Any, Iterable, Optional, List, Dict, Type
from collections import OrderedDict

from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.generic import View
from django.utils.text import slugify
from django.db.models import Q, Model
from django.shortcuts import render
from django.urls import reverse
from django import template

from .columns import BaseColumn, ColumnMethod, ColumnModel, ColumnChoice
from .meta import CustomAction, Filter
from .utils import CustomPaginator
from .forms import GenericForm


class DatatableMetaclass(type):
    @classmethod
    def _get_declared_fields(cls, bases, attrs) -> OrderedDict:
        """Get the declared fields for the class and return them in the order they were declared"""
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, BaseColumn)]

        fields.sort(key=lambda x: x[1]._creation_counter)

        known = set(attrs)

        def visit(name):
            known.add(name)
            return name

        base_fields = [
            (visit(name), f)
            for base in bases if hasattr(base, '_declared_fields')
            for name, f in base._declared_fields.items() if name not in known
        ]

        return OrderedDict(base_fields + fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_fields'] = cls._get_declared_fields(bases, attrs)
        return super().__new__(cls, name, bases, attrs)


class Datatable(View, metaclass=DatatableMetaclass):
    """A class to create a datatable"""
    #: Model to use for the datatable
    model: Model = None
    #: Table id used in the template (used to override the columns html too)
    table_id: str = None
    #: Table name to be used in the template
    table_name: str = None
    #: Path to the list template
    template_name = "datatable/list.html"

    #: Default icons. These can be overridden in the Meta class (delete_icon, update_icon)
    DEFAULT_UPDATE_ICON = "flaticon2-contract"
    DEFAULT_DELETE_ICON = "fa fa-trash-alt"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.validate_columns()
        self._custom_actions = self._get_custom_actions()
        self._filters = self._get_filters()

    class Meta:
        """Meta class for datatable"""

        #: Create url name defined in urls.py
        create_url_name: str = None
        #: Label for the create button
        create_url_label: str = "Adicionar"

        #: Delete url name defined in urls.py
        delete_url_name: str = None
        #: Delete url argument defined in urls.py (e.g. pk)
        delete_arg_name: str = None
        #: Delete icon used in actions dropdown
        delete_icon: str = None

        #: Update url name defined in urls.py
        update_url_name: str = None
        #: Update url argument defined in urls.py (e.g. pk)
        update_arg_name: str = None
        #: Update icon used in actions dropdown
        update_icon: str = None

        #: Create permission name
        create_permission: str = None
        #: Update permission name
        update_permission: str = None
        #: Delete permission name
        delete_permission: str = None

        #: List of custom filters to be used in the datatable
        filters: Dict[str, Filter] = None
        #: List of custom actions to be show in the datatable
        custom_actions: Iterable[CustomAction] = list()

        #: Defines if the entire datatable will be sortable or not
        sortable: bool = False

    def _get_custom_actions(self) -> List[dict]:
        """Get the custom actions for the class and return them in the order they were declared

        :return: The custom actions for the datatable
        :rtype: List[dict]
        """
        actions = getattr(self.Meta, "custom_actions", [])

        return [{
            "name": action.name,
            "identifier": slugify(action.name).replace("-", "_"),
            "icon": action.icon,
            "url_name": action.url_name,
            "arg_name": action.arg_name,
            "permission": action.permission,
            "show_function": action.show_function,
            "method": action.method,
            "target": action.target,
        } for action in actions] if actions else []

    def _get_filters(self) -> List[dict]:
        """Get the filters for the class and return them in the order they were declared

        :return: The filters for the datatable
        :rtype: List[dict]
        """
        filters = getattr(self.Meta, "filters", [])

        return [{
            "field": field,
            "label": filter.label,
            "type": filter.type,
            "initial": filter.initial,
            "queryset_filter_by": filter.queryset_filter_by,
            "queryset": filter.queryset,
        } for field, filter in filters.items()] if filters else []

    def get_columns(self) -> list:
        """Get the columns for the datatable

        :return: The columns for the datatable
        :rtype: list
        """
        columns = []

        for field, column in self._declared_fields.items():
            columns.append({
                "name": column.name or field,
                "field": field,
                "auto_hide": column.auto_hide,
                "sortable": column.orderable,
                "width": column.width,
                "align": column.align,
                "visible": column.visible,
            })


        actions = self.get_actions()

        if actions:
            columns.append({
                "name": "Acções",
                "field": "actions",
                "is_action": True,
                "sortable": False,
                "width": 50,
                "align": "center",
                "visible": True,
                "actions": actions,
            })

        return columns

    def get_action_information(
        self,
        name: str,
        identifier: str,
        icon: str,
        permission: str,
        method: str = "GET",
        target: str = "_self",
        is_delete: Optional[bool] = False
    ) -> dict:
        """Get the action information for a given action

        :param name: The name of the action
        :type name: str
        :param identifier: The identifier of the action
        :type identifier: str
        :param icon: The icon for the action
        :type icon: str
        :param permission: Permission to show the action
        :type permission: str
        :param method: The method of the action
        :type method: str
        :param target: The target of the action
        :type target: str
        :param is_delete: If the action is a delete action, defaults to False
        :type is_delete: Optional[bool], optional
        :return: The action information
        :rtype: dict
        """
        return {
            "name": name,
            "identifier": identifier,
            "icon": icon,
            "permission": permission,
            "is_delete": is_delete,
            "method": method,
            "target": target,
        }

    def get_default_actions(self) -> list:
        """Get the default actions for the datatable

        :return: The default actions for the datatable
        :rtype: list
        """
        default_actions: List[dict] = list()
        if getattr(self.Meta, "update_url_name", None):
            default_actions.append(self.get_action_information(
                name="Alterar",
                identifier="update_action",
                icon=getattr(self.Meta, "update_icon", self.DEFAULT_UPDATE_ICON),
                permission=getattr(self.Meta, "update_permission", self.update_permission),
            ))

        if getattr(self.Meta, "delete_url_name", None):
            default_actions.append(self.get_action_information(
                name="Eliminar",
                identifier="delete_action",
                icon=getattr(self.Meta, "delete_icon", self.DEFAULT_DELETE_ICON),
                permission=getattr(self.Meta, "delete_permission", self.delete_permission),
                is_delete=True,
            ))

        return default_actions

    def get_actions(self) -> list:
        """Get the actions for the datatable

        :return: The actions for the datatable
        :rtype: list
        """
        actions: list = self.get_default_actions()

        for action in self._custom_actions:
            actions.append(self.get_action_information(
                name=action["name"],
                identifier=action["identifier"],
                icon=action["icon"],
                permission=action["permission"],
                method=action["method"],
                target=action["target"],
            ))

        return actions

    def get_permissions(self) -> dict:
        """Get the permissions for the datatable

        :return: The permissions for the datatable
        :rtype: dict
        """
        user = self.request.user

        return {
            "can_create": user.has_perm(self.create_permission),
            "can_update": user.has_perm(self.update_permission),
            "can_delete": user.has_perm(self.delete_permission)
        }

    def get_extended_html_filepath(self) -> str:
        """Get the extended html filepath for the datatable. In this path you can add custom html
        to the datatable using the table id as the filename. For example, if the table id is
        `my_table`, the file should be named `my_table.js` and should be placed in the
        `templates/datatable/html` folder.

        :return: The extended html filepath for the datatable
        :rtype: str
        """
        return f"datatable/html/{self.table_id}.js"

    def have_extended_functions(self) -> bool:
        """Check if the datatable has extended functions. This will check if the file exists in the
        `templates/datatable/html` folder.

        :return: True if the datatable has extended functions, False otherwise
        :rtype: bool
        """
        try:
            template.loader.get_template(self.get_extended_html_filepath())
            return True
        except template.TemplateDoesNotExist:
            return False

    def get_context_data(self, **kwargs) -> dict:
        """Get the context data for the datatable. This will be called on the get method

        :param kwargs: Any extra context data to pass to the template
        :return: The context data for the datatable
        :rtype: dict
        """
        context = dict()

        context["table_id"] = self.table_id
        context["search_id"] = self.search_id
        context["name"] = self.table_name
        context["columns"] = self.get_columns()
        context["actions"] = self.get_actions()
        context["filters"] = self.get_filters_context()
        context["permissions"] = self.get_permissions()
        context["sortable"] = getattr(self.Meta, "sortable", None)
        context["create_url_label"] = getattr(self.Meta, "create_url_label", "Adicionar")
        context["extend_js"] = self.have_extended_functions()
        context["extended_filepath"] = self.get_extended_html_filepath()

        url = getattr(self.Meta, "create_url_name", None)

        if url:
            context["create_url"] = reverse(url)

        return context

    def validate_columns(self):
        """Validate all the columns needed for the datatable to work. This method can be
        refactored to add new validations. At this moment it only validates if the model and
        table id attributes are set.

        :raises: AssertionError if a column is missing or invalid
        """
        assert self.model is not None, "model is not set"
        assert self.table_id is not None, "table_id is not set"

    def get_queryset(self) -> Iterable[Model]:
        """Get the queryset for the datatable. This method can be overriden to add a custom
        queryset with annotated/aggregated fields. The annotated fields can be used in the
        datatable columns.

        :return: The queryset for the datatable
        :rtype: Iterable[Model]
        """
        return self.model.objects.all()

    def get_queryset_data(self) -> Iterable[Any]:
        """Get the queryset for the datatable. This method will get the original queryset
        from the get_queryset method and will apply the filters and search retrieved from
        the request.

        :return: The queryset for the datatable
        :rtype: Iterable[Any]
        """
        queryset = self.get_queryset()
        filters, order_by = self.get_filters_search()
        order_by = order_by or ["-pk"]
        return queryset.filter(filters).order_by(*order_by)

    def get_paginated_data(self) -> tuple:
        """Get the paginated data for the datatable. This uses a CustomPaginator that will
        get the total count of the queryset without retrieven all fields from the database.

        :return: The paginated data for the datatable
        (object_list, number_of_pages, current_page, number_of_columns)
        :rtype: tuple
        """
        queryset = self.get_queryset_data()
        search_data = self.get_search_data()
        paginator = CustomPaginator(queryset, search_data.get("per_page"))
        page = paginator.get_page(search_data.get("page"))

        return page.object_list, paginator.num_pages, page.number, queryset.count()

    @property
    def search_id(self) -> str:
        """Get the search id for the datatable

        :return: The search id for the datatable
        :rtype: str
        """
        return f"kt_datatable_{self.table_id}_search"

    @property
    def create_permission(self) -> str:
        """Get the create permission for the datatable using the app label and the model name

        :return: The create permission for the datatable
        :rtype: str
        """
        default = "{}.add_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "create_permission", None) or default

    @property
    def update_permission(self) -> str:
        """Get the update permission for the datatable using the app label and the model name

        :return: The update permission for the datatable
        :rtype: str
        """
        default = "{}.change_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "update_permission", None) or default

    @property
    def delete_permission(self) -> str:
        """Get the delete permission for the datatable using the app label and the model name

        :return: The delete permission for the datatable
        :rtype: str
        """
        default = "{}.delete_{}".format(self.model._meta.app_label, self.model._meta.model_name)
        return getattr(self.Meta, "delete_permission", None) or default

    def get_meta_context(self, actual_page: int, total_pages: int, total_records: int) -> dict:
        """Get the meta context from the request

        :param actual_page: The actual page of the datatable
        :param total_pages: The total pages of the datatable
        :param total_records: The total records of the datatable
        :return: The meta context for the datatable
        :rtype: dict
        """
        search_data = self.get_search_data()

        return {
            "page": actual_page,
            "pages": total_pages,
            "perpage": search_data.get("per_page"),
            "total": total_records,
            "sort": search_data.get("sort"),
            "field": search_data.get("sort_field"),
        }

    def get_column_context(self, column: Type[BaseColumn], field: str, obj) -> dict:
        """Get the column context for the datatable, this will be returned
        when the datatable script requests the column data via POST

        :param column: The column for the datatable
        :param field: The field for the datatable
        :param obj: The object for the datatable
        :return: The column context for the datatable
        :rtype: dict
        """
        context = dict()
        value = column.get_value(field, obj, self)
        url_attribute = value

        if type(column) == ColumnChoice:
            context[f"{field}_choice_label"] = column.get_choice_label(value)
        elif type(column) == ColumnModel:
            model = getattr(obj, field, None)
            url_attribute = getattr(model, column.url_attribute, None) if model else None

        url_name = getattr(column, "url_name", None)

        if url_attribute and url_name:
            url_arg = getattr(column, "url_arg", "pk")
            context[f"{field}_url"] = reverse(
                url_name, kwargs={url_arg: url_attribute}
            )

        context.update({f"{field}_name": column.name or field})
        context.update({f"{field}_visible": column.visible})
        context.update({f"{field}_auto_hide": column.auto_hide})
        context.update({f"{field}_width": column.width})
        context.update({field: value})
        return context

    def get_action_url(self, action: dict, arg_value: int | str) -> str:
        """Get the action url for the datatable

        :param action: The action for the datatable
        :param arg_value: The argument value for the action
        :return: The action url for the datatable
        :rtype: str
        """
        return reverse(
            action.get('url_name'),
            kwargs={action.get('arg_name'): arg_value}
        )

    def get_action_context(self, action: dict, obj: Type[Model]) -> dict:
        """Get the action context for the datatable

        :param action: The action for the datatable
        :param obj: The object instance
        :return: The action context for the datatable
        :rtype: dict
        """
        context = dict()
        identifier = action.get("identifier")
        attribute = action.get("show_function")
        permission = action.get("permission")
        show_function = getattr(self, attribute, None) if attribute else None
        arg_value = getattr(obj, action.get("arg_name"), obj.pk)

        context.update({f"{identifier}_name": action.get("name")})
        context.update({f"{identifier}_url": self.get_action_url(action, arg_value)})
        context.update({f"{identifier}_icon": action.get("icon")})
        context.update({f"{identifier}_show": show_function(obj) if show_function else True})
        context.update({f"{identifier}_perm": self.request.user.has_perm(permission)})
        context.update({"actions": identifier})

        return context

    def get_form_args_kwargs(self, request: HttpRequest) -> list:
        """Get the form args and kwargs for the datatable

        :param request: The request for the datatable
        :return: The form args for the datatable
        :rtype: list
        """
        form_context = dict()
        form_kwargs = {"fields": {}}

        for filter in self._filters:
            # If we have a request we will check if any of our filters are in the request
            if request:
                field = filter.get("field")

                # For some reason, django does not like the field name to be a list, so we
                # check if out filter can return a list and then we will get the list
                # appending [] to the field name
                if filter.get("type") in [Filter.MULTIPLE_CHOICES, Filter.MODEL_MULTIPLE_CHOICES]:
                    form_context[field] = request.POST.getlist(f"{field}[]")
                # If the filter is a single choice, we will check if the value exists in the
                # request and then we will retrieve the first value on the list. This was made
                # because the select from bootstrap was selecting by default the first value
                # and doesnt allow us to change it in a easy/clean way, so we set form field 
                # for CHOICES and MODEL_CHOICES SelectMultiple with max-choices=1, so it will
                # return a list with one value.
                elif filter.get("type") in [Filter.CHOICES, Filter.MODEL_CHOICES]:
                    field_value = request.POST.getlist(f"{field}[]")

                    if field_value:
                        form_context[field] = field_value[0]
                else:
                    form_context[field] = request.POST.get(field)

            form_kwargs["fields"].update({
                filter.get("field"): {
                    "label": filter.get("label"),
                    "type": filter.get("type"),
                    "initial": filter.get("initial"),
                    "queryset_filter_by": filter.get("queryset_filter_by"),
                    "queryset": filter.get("queryset"),
                }
            })

        return (form_context, form_kwargs)

    def get_filters_context(self, request: Optional[HttpRequest] = None) -> dict:
        """Get the filters context for the datatable

        :param request: The request for the datatable
        :return: The filters context for the datatable
        :rtype: dict
        """
        form_args, form_kwargs = self.get_form_args_kwargs(request)
        return GenericForm(form_args, **form_kwargs) if form_kwargs else None

    def get_column_data(self, obj) -> dict:
        """Get the column data for the datatable.

        :param obj: The object for the datatable
        :return: The column data for the datatable
        :rtype: dict
        """
        # DT_RowId will always be the primary key of the object
        column_data = {"DT_RowId": obj.id}

        # We will loop through all the columns and get the context for each one
        for field, column in self._declared_fields.items():
            column_data.update(self.get_column_context(column, field, obj))

        # Then we will loop the actions and get the context for each one
        for action in self._custom_actions:
            column_data.update(self.get_action_context(action, obj))

        # Then we get the default actions (update and delete)
        url = getattr(self.Meta, "update_url_name", None)
        if url:
            arg_name = getattr(self.Meta, "update_arg_name", None) or "pk"
            update_permission = getattr(self.Meta, "update_permission", self.update_permission)
            column_data.update({
                "update_action_url": reverse(url, kwargs={arg_name: obj.pk}),
                "update_action_show": True,
                "update_action_perm": self.request.user.has_perm(update_permission),
            })

        url = getattr(self.Meta, "delete_url_name", None)
        if url:
            arg_name = getattr(self.Meta, "delete_arg_name", None) or "pk"
            delete_permission = getattr(self.Meta, "delete_permission", self.delete_permission)
            column_data.update({
                "delete_action_url": reverse(url, kwargs={arg_name: obj.pk}),
                "delete_action_show": True,
                "delete_action_perm": self.request.user.has_perm(delete_permission),
            })

        return column_data

    def get_data_context(self, object_list: Iterable[Type[Model]]) -> list:
        """Get the data context for the datatable, this will be used in POST 
        requests called from the datatable

        :param object_list: The object list for the datatable
        :return: The data context for the datatable
        :rtype: list
        """
        return [self.get_column_data(obj) for obj in object_list]

    def process_response(self) -> dict:
        """Process the response for the datatable, call the needed methods to build
        the data structure needed to process the datatable. {data: [], meta: {}}

        :return: The response for the datatable
        :rtype: dict
        """
        object_list, total_pages, actual_page, total_records = self.get_paginated_data()
        meta = self.get_meta_context(actual_page, total_pages, total_records)
        data = self.get_data_context(object_list)
        return {"meta": meta, "data": data}

    def get_filters_search(self) -> list:
        """Get the queryset data for the datatable. This function is generic and manages all
        the fields like a string (Unless you have defined the search_type like DATE types)

        :return: The queryset data for the datatable
        :rtype: list
        """
        search_data = self.get_search_data()
        filters = Q()
        order_by = []
        order_type = "" if search_data.get("sort", "desc") == "desc" else "-"

        for field, column in self._declared_fields.items():
            if type(column) == ColumnMethod:
                continue

            lookup_fields = [""]

            if type(column) == ColumnModel:
                lookup_fields = column.lookup_fields

            # We will split the search data by comas and then we will loop through each one
            queries = search_data.get("query", [])
            if queries:
                queries = queries.split(",")

            if column.searchable and queries:
                group = Q()

                for lookup in lookup_fields:
                    if not lookup:
                        param = f"{field}__{column.search_type}"
                    else:
                        param = f"{field}__{lookup}__{column.search_type}"

                    for query in queries:
                        if lookup:
                            group |= Q(**{param: query.strip()})
                        else:
                            group &= Q(**{param: query.strip()})

                filters |= group

            if column.orderable and field == search_data.get("sort_field"):
                order_by.append(f"{order_type}{field}")

        if self._filters:
            form = self.get_filters_context(self.request)
            if form.is_valid():
                filters &= form.get_filters()
            else:
                raise Exception(form.errors)

        return filters, order_by

    def get_search_data(self) -> dict:
        """Get the search data from the request body. This data is suposed to be sent by
        the datatable script via POST request.

        :return: The search data from the request body
        :rtype: dict
        """
        return {
            "query": self.request.POST.get(f"query[{self.search_id}]"),
            "page": self.request.POST.get("pagination[page]"),
            "pages": self.request.POST.get("pagination[pages]"),
            "per_page": self.request.POST.get("pagination[perpage]"),
            "total": self.request.POST.get("pagination[total]"),
            "sort": self.request.POST.get("sort[sort]"),
            "sort_field": self.request.POST.get("sort[field]"),
        }

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """Process the POST request for the datatable. This method is called by the datatable

        :param request: The request for the datatable
        :param args: The args for the datatable
        :param kwargs: The kwargs for the datatable
        :return: The response for the datatable
        :rtype: HttpResponse
        """
        response = self.process_response()
        return JsonResponse(response)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """Process the GET request for the datatable

        :param request: The request for the datatable
        :param args: The args for the datatable
        :param kwargs: The kwargs for the datatable
        :return: The response for the datatable
        :rtype: HttpResponse
        """
        return render(request, self.template_name, self.get_context_data())
