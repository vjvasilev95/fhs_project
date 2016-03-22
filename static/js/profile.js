$(document).ready(function() {

    $.fn.bootstrapSwitch.defaults.onText = 'Yes';
    $.fn.bootstrapSwitch.defaults.offText = 'No';
    $.fn.bootstrapSwitch.defaults.size = 'normal';
    $("[name='shared-checkbox']").bootstrapSwitch();

    $('input[name="shared-checkbox"]').on('switchChange.bootstrapSwitch', function (event, state) {

        var cat_id = $(this).data('id');
        var csrftoken = Cookies.get('csrftoken');

        $.post('/fhs/update-category-state/', {'state': state, 'id': cat_id, csrfmiddlewaretoken: csrftoken},
            function (data) {
            });
    });
});