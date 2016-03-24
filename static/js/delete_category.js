
$(document).ready(function(){

    $('.delete-btn').click(function(event){
        event.preventDefault();
        var theRow = $(this).parent().parent();
        var theTable = theRow.parent();
        var theColumn = $(this).parent();
        var cat_id = theColumn.siblings().find('.cat-info').attr('value');
        var csrftoken = Cookies.get('csrftoken');

        $.post('/fhs/delete-category/', {'cat_id': cat_id, csrfmiddlewaretoken: csrftoken},
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