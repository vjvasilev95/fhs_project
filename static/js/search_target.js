$(document).ready(function() {

    $.fn.bootstrapSwitch.defaults.onText = 'Yes';
    $.fn.bootstrapSwitch.defaults.offText = 'No';
    $.fn.bootstrapSwitch.defaults.size = 'small';
    //$("[name='search-target-nonchecked']").bootstrapSwitch();
    $("[name='search-target']").bootstrapSwitch();
//    $("#search-form-info").hide();


    $('input[name="search-target"]').on('switchChange.bootstrapSwitch', function (event, state) {
        if(!state){
            document.getElementById("age").required = true;
            document.getElementById("gender").required = true;
            $("#search-form-info").fadeIn(800);
            $('#age').addClass('important');

        }else{
            document.getElementById("age").required = false;
            document.getElementById("gender").required = false;
            $("#search-form-info").hide();
            $('#age').removeClass('important');
        }
        $("#age").val("");

//        $("#gender").val("None");
    });

    $('#info-trigger').on('click', function(e) {
        $('#info-search').toggle();
    });

});