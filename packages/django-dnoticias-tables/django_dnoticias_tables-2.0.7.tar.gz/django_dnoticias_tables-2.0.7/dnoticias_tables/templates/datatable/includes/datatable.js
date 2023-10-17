{% load i18n tables %}

function toggleFilters() {
    let $switchIcon = $("#advanced-search").find('.fa');

    if ($switchIcon.hasClass('fa-caret-square-down')) {
        $switchIcon.attr('class', 'fa fa-minus-square');
    } else {
        $switchIcon.attr('class','fa fa-caret-square-down');
    }

    $('.filter-elements').slideToggle(200);
}


function get_action_item({url, name, icon, id=null, method="GET", target="_self"}) {
    let htmlAction = ``;

    let htmlButton = `
        <i class="kt-nav__link-icon ${icon}"></i>\
        <span class="kt-nav__link-text">${name}</span>\
    `;

    if (method !== "GET") {
        htmlAction = `<form id="form_actions_${id}" action="${url}" method="${method}" class="kt-nav__link">\
            {% csrf_token %}
            <a href="javascript:;" onclick="parentNode.submit();" data-id="${id}" class="kt-nav__link">\
                ${htmlButton} \
            </a>\
        </form>`;
    } else {
        htmlAction = `
            <a href="${url}" data-id="${id}" target="${target}" class="kt-nav__link">\
                ${htmlButton} \
            </a>\
        `;
    }

    return `
        <li class="kt-nav__item">
            ${htmlAction}\
        </li>`;
}

function get_delete_item({name, url, icon, id}) {
    return `
    <li class="kt-nav__item">\
        <a href="javascript:;" data-toggle="popover" data-pk="${id}" data-model="edition" data-link="${url}" data-redirect="${location.href}" data-id="${id}" class="delete-action kt-nav__link">\
            <i class="kt-nav__link-icon ${icon}"></i>\
            <span class="kt-nav__link-text">${name}</span>\
        </a>\
    </li>
    `;
}

function getExtraParams(){
    {% for field in filters %}
    let {{field.auto_id}} = $('#{{field.auto_id}}').val();
    {% endfor %}

    let extraParams = {
        {% for field in filters %}
        "{{field.html_name}}": {{field.auto_id}},
        {% endfor %}
    };

    console.log("extra params:", extraParams)
    return extraParams
}

let KTDashboard = function () {
    let datatable
    let datatableEmailsList = function () {
        if ($('#{{ table_id }}').length === 0) {
            return;
        }
        
        let extraParams = getExtraParams();
        datatable = $('.kt-datatable').KTDatatable({
            data: {
                type: 'remote',
                source: {
                    read: {
                        url: '{{ request.path }}',
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}',
                        },
                        params: extraParams,
                    }
                },
                pageSize: 10,
                saveState: {
                    cookie: false,
                    webstorage: true
                },
                serverPaging: true,
                serverFiltering: true,
                serverSorting: true
            },
            translate: {
                records: {
                    processing: "{% trans 'Carregando...' %}",
                    noRecords: "{% trans 'Sem resultados' %}",
                },
                toolbar: {
                    pagination: {
                        items: {
                            default: {
                                first: "{% trans 'Início' %}",
                                prev: "{% trans 'Anterior' %}",
                                next: "{% trans 'Seguinte' %}",
                                last: "{% trans 'Último' %}",
                                more: "{% trans 'Mais páginas' %}",
                                input: "{% trans 'Página número' %}",
                                select: "{% trans 'Tamanho da página' %}",
                                all: "{% trans 'tudo' %}",
                            },
                            info: "",
                        },
                    },
                },
            },
            layout: {
                scroll: false,
                //height: 500,
                footer: false,
            },
            sortable: "{{ sortable }}" == "True",

            search: {
                input: $('#{{ search_id }}'),
            },

            pagination: true,
            columns: [
                {% for column in columns %}
                    {% include "../includes/column.html" with column=column only %}
                {% endfor %}
            ]
        });

        datatable.on("kt-datatable--on-layout-updated", function(event, data){
            setDeleteActionHandlers();
            
            $('[data-toggle="kt-tooltip"]').each(function() {
                KTApp.initTooltips();
            });
            document.dispatchEvent(new Event('kt-layout-updated'));
        });
    }

    return {
        init: function () {
            datatableEmailsList();
            var loading = new KTDialog({ 'type': 'loader', 'placement': 'top center', 'message': '{% trans "Carregando ..." %}' });
            loading.show();
            let value = "";

            {% for field in filters %}
            value = datatable.getDataSourceParam("{{ field.html_name }}");

            if (value !== null && value.length > 0) {
                $('#{{ field.auto_id }}').val(value);
                $('#{{ field.auto_id }}').selectpicker("refresh");
                toggleFilters();
            }
            {% endfor %}

            setTimeout(function () {
                loading.hide();
            }, 3000);
        },
        setDataSourceParamAndLoad: function(extraParamsContext){
            for (let key in extraParamsContext) {
                if (extraParamsContext.hasOwnProperty(key)) {
                    datatable.setDataSourceParam(key, extraParamsContext[key]);
                }
            }
            let paginationContext = datatable.getDataSourceParam("pagination");
            paginationContext.page = 1;
            datatable.setDataSourceParam("pagination", paginationContext);

            datatable.load();
        }
    };
}();

KTDashboard.init();

function OnTriggerChangesFilterChanges(){
    let extraParams = getExtraParams();
    KTDashboard.setDataSourceParamAndLoad(extraParams);
}

$('.selectpicker').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
    OnTriggerChangesFilterChanges();
});

$("input[class*='daterange']").on("apply.daterangepicker change", function (ev, picker) {
    OnTriggerChangesFilterChanges();
});

$("input[class*='date']").on("changeDate change", function (ev, picker) {
    OnTriggerChangesFilterChanges();
});

$('.remove-filters').on('click', function(event){
    event.preventDefault();
    $('.selectpicker').selectpicker('deselectAll');
    $('#{{ search_id }}').val('');
    $('input[class*="daterange"]').val('');
    $('input[class*="datepicker"]').val('');
    
    OnTriggerChangesFilterChanges();
    resetSelectpickers();resetSelectpickers();resetSelectpickers();
});

$('#advanced-search').on('click', function(event){
    event.preventDefault();
    toggleFilters();
});