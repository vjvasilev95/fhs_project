
$(document).ready(function(){

    $('.delete-btn').click(function(event){
        event.preventDefault();

        var theRow = $(this).parent().parent();

        var theTable = theRow.parent();
        var theColumn = $(this).parent();

        var cat_name = theColumn.siblings().find('.cat-info').attr('value');
//        alert("we clicked the delete button")
        var csrftoken = Cookies.get('csrftoken');

        $.post('/fhs/delete-category/', {'cat_name': cat_name, csrfmiddlewaretoken: csrftoken},
         function(data){
                    var response = $.parseJSON(JSON.stringify(data));
                    if (response['response'] == 'Success'){
                        theRow.fadeOut(1300, function(){ theRow.remove(); });
                    } else {
                        alert("The was a problem with the server while trying to delete the category.");
                    }
                });
    });

});