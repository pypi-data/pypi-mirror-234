{% load i18n %}

function setDeleteActionHandlers(){
    $('.delete-action').popover({
        title : "<span>{% trans 'Confirmação' %}</span>",
        html: true,
        container: 'body',
        content :   `<div class="row">
                        <div class="col-lg-12">
                            Pretende eliminar pemanentemente este registo? Esta acção é irreversível.
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div class="col-lg-6">
                            <a href="#" tabindex="0" class="close-popover btn btn-secondary w-100">Cancelar</a>
                        </div>
                        <div class="col-lg-6">
                            <a href="#" tabindex="0" class="post-delete btn btn-danger text-white w-100"><i class="kt-nav__link-icon fa fa-trash"></i> Eliminar</a>
                        </div>
                    </div>`
    });

    $('.delete-action').on('shown.bs.popover', function () {
        var popoverId = $(this).attr("aria-describedby");
        $("#"+popoverId).attr("data-model", $(this).attr("data-model"));
        $("#"+popoverId).attr("data-pk", $(this).attr("data-pk"));
        console.log("shown.bs.popover");
    });
}

setDeleteActionHandlers();

$('body').on('click', function (e) {
    //did not click a popover toggle or popover
    var isDeleteActionButton = false;
    var navItem = $(e.target).parents(".kt-nav__item");
    if(navItem.length){
        var deleteAction = navItem.find(".delete-action");
        isDeleteActionButton = deleteAction ? true : false;
    }
    if ($(e.target).data('toggle') !== 'popover' && $(e.target).parents('.popover').length === 0 && !isDeleteActionButton) {
        $('[data-toggle="popover"]').popover('hide');
    }
});

$(document).on("click", ".post-delete", function(event){
    event.preventDefault();
    var popover = $(this).closest(".popover");
    var model = popover.attr("data-model");
    var pk = popover.attr("data-pk");
    var deleteButton = $('.delete-action[data-model="'+ model +'"][data-pk="'+ pk +'"]');
    var context = {};
    $.each(deleteButton[0].attributes, function() {
        if(this.specified && this.name.startsWith("data-")) {
            context[this.name.replace("data-","")] = this.value;
        }
    });
    var deleteLink = deleteButton.attr("data-link");
    var ajaxAttr = deleteButton.attr("data-ajax")
    var isAjax = false;
    if(ajaxAttr){
        isAjax = ajaxAttr.toLowerCase() == "true";
    }
    if(isAjax){
        $.post(deleteLink, context, function(data, status, xhr){
            if(typeof OnDeletePopoverAjaxHandler === 'function') {
                OnDeletePopoverAjaxHandler(data, status, xhr, model, pk);
            }else{
                console.log("The delete popover handler was not defined!");
            }
        })
    }else{
        post(deleteLink, context);
    }
});
$(document).on("click", ".close-popover", function(event){
    event.preventDefault();
    $('.delete-action').popover('hide');
});

$(document).on("click", ".dropdown-menu .delete-action", function(event){
    event.preventDefault();
    event.stopPropagation();
});
