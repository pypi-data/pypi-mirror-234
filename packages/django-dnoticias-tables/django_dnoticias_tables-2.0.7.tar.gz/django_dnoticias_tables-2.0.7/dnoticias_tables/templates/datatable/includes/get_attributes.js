function getAttributes(element){
    var context = {};
    try {
        $.each($(element)[0].attributes, function() {
            if(this.specified && this.name.startsWith("data-")) {
                context[this.name.replace("data-","")] = this.value;
            }
        });
    } catch (error) {
        console.log(error)
    }
    return context
}
