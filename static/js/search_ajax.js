$(document).ready(function(){
    $('.save-btn').click(function(e){

        e.preventDefault();
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
    });
}); 