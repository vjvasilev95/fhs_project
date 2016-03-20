var suggestCallBack; // global var for autocomplete jsonp
$(document).ready(function(){


    $('.save-btn').click(function(e){

        e.preventDefault();

        if ($(this).siblings('.category-choice').length) {
            var csrftoken = Cookies.get('csrftoken');

            var info = $(this).siblings('.hidden-info');
            var url = info[0].value;
            var title = info[1].value;
            var summary = info[2].value;
            var source = info[3].value;
//            console.log(source);
            var category = $(this).siblings('.category-choice').find(":selected").text();
            var button = $(this);

            $.post('/fhs/save-page/', {'url': url, 'title': title, 'summary': summary,
                    'category': category, 'source': source, csrfmiddlewaretoken: csrftoken},
                function(data) {
                    button.next().remove();
                    var response = $.parseJSON(JSON.stringify(data));
                    console.log(response);
                    if (response['response'] == "Existent page") {
                        button.after("<span class='save-msg-existent'>This page is already existent in category " + "<a class='save-msg-existent-url' href='/fhs/category/"+response['category']+"'>" + category +"</a>" + "</span>");
                    } else if (response['response'] == "Problem while fetching the resource") {
                        button.after("<span class='save-msg-error'>There was a problem while fetching the resource. We are sorry for the inconvenience.</span>");
                    } else {
                        button.after("<span class='save-msg-success'>Page is saved in category " + "<a href='/fhs/category/"+response['category']+"'>" + category +"</a>" + "</span>");
                    }
                });
        } else {
            $(this).siblings('.create-new-category-wrapper').show();
        }
    });

    $('.submit-new').click(function(e){

        e.preventDefault();

        var csrftoken = Cookies.get('csrftoken');

        var info = $(this).siblings('.new-cat-info');
        var name = info[0].value;

        var description = info[1].value;
        var shared = $('.new-cat-info-btn').is(':checked');
        var button = $(this);
        var wrapper = button.parent();

        $.post('/fhs/add_category/', {'name': name, 'description': description, 'shared': shared,
                csrfmiddlewaretoken: csrftoken},

                function(data) {

                    if (data == "Success"){

                        // Get the save page button element
                        var save_btn = wrapper.siblings('.save-btn').first();

                        // Remove all the forms
                        $('.create-new-category-wrapper').remove();

                        // Append the success message
                        save_btn.after("<span class='save-msg-success'>Category successfully created.</span");

                        // Update the template to show the new category everywhere
                        $('.save-btn').before("<select name='category' class='category-choice' required>"+
                        "<option value=" + name + ">" + name + "</option>"+
                        "</select>");
                    } else {
                        button.after("<span class='save-msg-error'>A category with that name already exists.</span");
                    }

                });

    });

    $('#suggestion').keyup(function(){
        var query;
        var data = $(this).data('page');
        query = $(this).val();
        if (!query) {
            $('.public-cats').show();
            $('#cats').hide();
        }
        $.get('/fhs/suggest_category/', {suggestion: query, page: data}, function(data){

            $('.public-cats').hide();
            $('#cats').show();

            $('#cats').html(data);
        });
    });

    $("#query").autocomplete({
        source: function(request, response) {
            $.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
                {
                  "hl":"en", // Language
                  "jsonp":"suggestCallBack", // jsonp callback function name
                  "q":request.term, // query term
                  "client":"youtube" // force youtube style response, i.e. jsonp
                }
            );
            suggestCallBack = function (data) {
                var suggestions = [];
                $.each(data[1], function(key, val) {
                    suggestions.push({"value":val[0]});
                });
                suggestions.length = 5; // prune suggestions list to only 5 items
                response(suggestions);
                $('.ui-helper-hidden-accessible').remove();
            };
        }
    });
}); 