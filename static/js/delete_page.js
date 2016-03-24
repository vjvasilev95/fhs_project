
$(document).ready(function(){

    $('.delete-btn').click(function(event){
        event.preventDefault();
        var theRow = $(this).parent().parent();
        var theTable = theRow.parent();
        var theColumn = $(this).parent();
        var page_title = theColumn.siblings().find('.page-info').attr('value');
        var cat_id = theColumn.siblings().find('.cat-info').attr('value');
        var csrftoken = Cookies.get('csrftoken')

        $.post('/fhs/delete-page/', {'cat_id': cat_id, 'page_title': page_title, csrfmiddlewaretoken: csrftoken},
         function(data){

            var response = $.parseJSON(JSON.stringify(data));
            if (response['response'] == 'Success'){
                  if(response['pages_count'] == 0){
                    $('#cat_views_paragraph').after("<strong>No pages currently in category.</strong>");
                  }
                theRow.fadeOut(1300, function(){ theRow.remove(); });
            } else {
                alert("There was a problem with the server while trying to delete the page.");
            }
        });
    });

});