
# dnoticias.pt - Tables

This package is used to a more dev-friendly datatable management.




## Datatable (new)
The datatable package has been created trying to maintain a consistent logic between the django projects. This new module have the following files:

datatable.py: Where all the backend logic is.

datatable.js: The datatable JS init. This will use the data constructed by the datatable.py different classes to render the datatable.

(optional) /datatable/html/{table-id}/index.js: This will contains all the extended functions used in the datatable.js rendering.

### How it works
To use the new datatable module you need to import it into your django views.py file and declare the class:

```py
from dnoticias_tables.datatable import Datatable, Column

class MyCustomDatatable(Datatable):
    id = Column(name="ID", orderable=True, searchable=True)
    email = Column(name="Email", searchable=True, width=150)

    model = User
    table_id = "user"

    class Meta:
        sortable = True
```

And then you need to define the view request path in your urls.py file:

```py
from . import views

urlpatterns = [
    ...
    path("datatable/", views.MyCustomDatatable.as_view(), name="datatable-list"),
]
```

And now its done, if you access to http://example.com/datatable/ the datatable is already rendering!

### Classes

#### Meta
The Meta class is used to redefine custom general variables used in the datatable.

Variables that you can define:

``` py
create_url_name = None  # Create url used in the datatable top corner button
delete_url_name = None  # Delete url used in each datatable row to delete an entry
update_url_name = None  # Update url used in each datatable row to update an entry

# Permissions (this uses the django permissions (i.e: "user.change_user"))
# Need to be a str
create_permission = None
update_permission = None
delete_permission = None

# Defines if the datatable can be sortable or not (even if you create any row with
# the orderable attribute in True, if the sortable variable is set to False, the
# table will not be sortable)
sortable = False
```

#### Column

Used to define a row in the datatable. The variable where the Column class is allocated need to have the same name as the object attribute you want to retrieve. i.e:

Having the following code:

```py
...
id = Column(name="ID", orderable=True, searchable=True)
email = Column(name="Email", searchable=True, width=150)

model = User
...
```

Means that the User model has the id and email attributes.

Parameters:

```py
name: Optional[str] = None,  # Name showed on the table header
searchable: Optional[bool] = False,  # Define if the row can be searchable
search_type: Optional[str] = FilterType.ICONTAINS,  # Filter type
visible: Optional[bool] = True,  # Define if the row is visible or not
auto_hide: Optional[bool] = False,  # Define if the row will autohide on responsive
orderable: Optional[bool] = False,  # Define if the row can be orderable
datetime_format: Optional[str] = "%d/%m/%Y %H:%M",  # Datetime format in case if the row is a datetime
width: Optional[int] = 100,  # Table row width
align: Optional[str] = "left"  # Table row align
```

#### ColumnMethod
Almost the same as **Column** but this uses a custom method instead of an object attribute.

This works like DRF serializer method do. You just need to create a method inside the view class
called get_**attribute**(self, obj) where obj is the current row.

You can  define a custom method using the *method* parameter

Parameters:

```py
method: Optional[str] = None,  # Method name (uses get_{attribute}) by default
name: Optional[str] = None,
visible: Optional[bool] = True,
searchable: Optional[bool] = True,
search_value: Optional[str] = None,
auto_hide: Optional[bool] = False,
orderable: Optional[bool] = False,
datetime_format: Optional[str] = "%d/%m/%Y %H:%M",
width: Optional[int] = 100,
align: Optional[str] = "left",
```

#### ColumnChoice
And again, almost the same as **Column** but this is used to display a choice field.
The only difference between this class and Column is that this class will receive a choices parameter and will return the choice label
used to display the data on the datatable. This will works **only and only** with the django choice classes.

*I.E: MyCustomStatusChoices.choices*

```py
choices: Optional[Iterable[tuple]] = None,
name: Optional[str] = None,
searchable: Optional[bool] = False,
search_type: Optional[str] = FilterType.ICONTAINS,
visible: Optional[bool] = True,
auto_hide: Optional[bool] = False,
orderable: Optional[bool] = False,
width: Optional[int] = 100,
align: Optional[str] = "left",
```

## Response

The response data can be used on custom functions (extend.js) so i think is important to
you know the structure.


```js
{
    "meta": {
        "page": 1,  // Actual page
        "pages": 34,  // Total pages
        "perpage": "10",  // Items shown per page (defined on datatable)
        "total": 334,  // Total items
        "sort": "asc",  // Current sort type
        "field": "title"  // Current sort field
    },
    "data": [
        {
            "DT_RowId": 1,  // DT row id
            "email_name": "Título",  // Column name defined on view
            "email_visible": true,  // Column visible defined on view
            "email_auto_hide": false,  // Autohide defined on view
            "email_width": 200,  // Column width defined on view
            "email": "example@mail.com",  // Column value for 'email'
            "status_choice_label": "Confirmado",  // Choice label (returned only on ColumnChoice!)
            "status_name": "Estado",
            "status_visible": true,
            "status_auto_hide": false,
            "status_width": 100,
            "status": "confirmed",
            "created_at_name": "Data de criação",
            "created_at_visible": true,
            "created_at_auto_hide": false,
            "created_at_width": 100,
            "created_at": "21/04/2021 13:24"
        },
        ...
    ]
}
```

## Using custom HTML per row

To define a custom html for any row, you need to create a file called extend.js on the following path:

`/your-project/templates/datatable/html/{table-id}/index.js` where table-id is the same as you defined on the view class.

The extend.js structure is quite simple, you just need to define a function that will return the html used for that row.

i.e:
```js
function get_status_html(data) {
    switch(data.status){
        case "pending":
            return '<span class="btn btn-bold btn-sm btn-font-sm btn-pill btn-label-brand">'+ data.status_choice_label +'</span>';
        case "confirmed":
            return '<span class="btn btn-bold btn-sm btn-font-sm btn-pill btn-label-success">'+ data.status_choice_label +'</span>';
    }
}
```

The function need to be called as "get_**attribute**_html(data)" where attribute is the attribute row you want to modify.

*Note that the 'data' parameter will contain all the row data, not only the required one.*

# TO-DO

[] Allow using custom filters like select
