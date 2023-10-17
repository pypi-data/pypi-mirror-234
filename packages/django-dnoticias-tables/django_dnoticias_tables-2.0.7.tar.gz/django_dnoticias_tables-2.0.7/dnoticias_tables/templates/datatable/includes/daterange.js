$('input[class*="daterange"]').daterangepicker({
    timePicker: true,
    autoUpdateInput: false,
    locale: {
        format: 'YYYY-MM-DD HH:mm',
        applyLabel: "Aplicar",
        cancelLabel: "Limpar",
        fromLabel: "Desde",
        toLabel: "Até",
        weekLabel: "S",
        separator: " até ",
        daysOfWeek: [
            "Dom",
            "Seg",
            "Ter",
            "Qua",
            "Qui",
            "Sex",
            "Sab",
        ],
        monthNames: [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ],
        firstDay: 1
    }
});

$('input[class*="daterange"]').on('apply.daterangepicker', function(ev, picker) {
    $(this).val(picker.startDate.format('YYYY-MM-DD HH:mm') + ' até ' + picker.endDate.format('YYYY-MM-DD HH:mm'));
});


$('input[class*="daterange"]').on('cancel.daterangepicker', function(ev, picker) {
    $(this).val('');
});