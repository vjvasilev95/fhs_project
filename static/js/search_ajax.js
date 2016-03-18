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
            var category = $(this).siblings('.category-choice').find(":selected").text();
            var button = $(this);

            $.post('/fhs/save-page/', {'url': url, 'title': title, 'summary': summary,
                    'category': category, 'source': source, csrfmiddlewaretoken: csrftoken},
                function(data) {
                    button.next().remove();
                    if (data == "Existent page") {
                        button.after("<span class='save-msg-existent'>This page is already existent in this category.</span>");
                    } else if (data == "Problem while fetching the resource") {
                        button.after("<span class='save-msg-error'>There was a problem while fetching the resource. We are sorry for the inconvenience.</span>");
                    } else {
                        button.after("<span class='save-msg-success'>Page is saved in category " + "<a href='#'>" + category +"</a>" + "</span>");
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
        query = $(this).val();
        if (!query) {
            $('.public-cats').show();
            $('#cats').hide();
        }
        $.get('/fhs/suggest_category/', {suggestion: query}, function(data){

            $('.public-cats').hide();
            $('#cats').show();

            $('#cats').html(data);
        });
    });

}); 