var suggestCallBack; // global var for autocomplete jsonp
$(document).ready(function(){
    $('.fa-spinner').addClass('hidden');
    $('.no-cats').hide();

    $('.category-choice').change(function() {
        var selection = $(this);
        var wrapper;

        if (selection.siblings('.create-new-category-wrapper').length) {
            wrapper = selection.siblings('.create-new-category-wrapper');
        } else {
            wrapper = selection.parent().siblings('.create-new-category-wrapper');
        }

        var save_btn = selection.next();
        if (selection.find(":selected").attr('value') == "new-cat") {
            save_btn.prop('disabled', true);
            wrapper.show();
        } else {
            save_btn.prop('disabled', false);
            wrapper.hide();
        }
    });

    $('.save-btn').click(function(e){

        e.preventDefault();
        if (!$(this).siblings('.category-choice').hasClass("no-cats")) {
            var csrftoken = Cookies.get('csrftoken');

            var info = $(this).siblings('.hidden-info');
            var url = info[0].value;
            var title = info[1].value;
            var summary = info[2].value;
            var source = info[3].value;
            var category = $(this).siblings('.category-choice').find(":selected").text();
            var button = $(this);


            $.post('/fhs/save-page/', {'url': url, 'title': title, 'summary': summary,
                    'category': category, 'source': source, csrfmiddlewaretoken: csrftoken},
                function(data) {

                    if (!button.next().hasClass('fa')){
                            button.next().remove();
                        }

                    var response = $.parseJSON(JSON.stringify(data));

                    if (response['response'] == "Existent page") {
                        button.after("<span class='save-msg-existent'>This page is already existent in category " + "<a class='save-msg-existent-url' href='/fhs/category/"+response['category']+"'>" + category +"</a>" + "</span>");
                    } else if (response['response'] == "Problem while fetching the resource") {
                        button.after("<span class='save-msg-error'>There was a problem while fetching the resource. We are sorry for the inconvenience.</span>");
                    } else {
                        button.after("<span class='save-msg-success'>Page is saved in category " + "<a href='/fhs/category/"+response['category']+"'>" + category +"</a>" + "</span>");
                    }
                });
        } else {
            $(this).parent().siblings('.create-new-category-wrapper').show();
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
        var wrapper = button.parent().parent();

        $.post('/fhs/add_category/', {'name': name, 'description': description, 'shared': shared,
                csrfmiddlewaretoken: csrftoken},

                function(data) {
                    var response = $.parseJSON(JSON.stringify(data));

                    if (response['response'] == "Success"){

                        // Get the save page button element
                        var save_btn = wrapper.siblings('.save_page_form').children('.save-btn').first();

                        // Hide all the forms
                        $('.create-new-category-wrapper').hide();

                        // Remove previous messages
                        if (!save_btn.next().hasClass('fa')){
                            save_btn.next().remove();
                        }
                        button.next().remove();

                        // Append the success message
                        save_btn.after("<span class='save-msg-success'>Category " + "<a href='/fhs/category/"+response['category']+"'>" + name +"</a>" + " successfully created.</span");

                        // Update the list of options
                        var select_tag_chosen = wrapper.siblings('.save_page_form').children('.category-choice');
                        var select_tag = $('.category-choice');
                        select_tag.append($("<option></option>").val(name).text(name));
                        select_tag_chosen.val(name);
                        $('.no-cats').show();

                        if (select_tag.hasClass('no-cats')) {
                            select_tag.removeClass('no-cats');
                        }
                        save_btn.prop('disabled', false);

                        $('.add_category').trigger("reset");
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
/* show spinner */
$( document ).ajaxStart(function() {
    $('.fa-spinner').removeClass('hidden');
});
/* hide spinner */
$( document ).ajaxStop(function() {
    $('.fa-spinner').addClass('hidden');
});
