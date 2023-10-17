{% include "../includes/get_attributes.js" %}
$(document).on("click", ".post-link", function(event){
    event.preventDefault();
    post($(this).attr("data-link"), getAttributes($(this)));
});
