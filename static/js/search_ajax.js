$(document).ready(function(){
    $('.save-btn').click(function(e){

        e.preventDefault();
        var csrftoken = Cookies.get('csrftoken');

        var info = $(this).siblings('.hidden-info');
        url = info[0].value;
        title = info[1].value;
        summary = info[2].value;
        source = info[3].value;
        category = $(this).siblings('.category-choice').find(":selected").text();

        $.post('/fhs/save-page/', {'url': url, 'title': title, 'summary': summary,
                'category': category, 'source': source, csrfmiddlewaretoken: csrftoken},
            function(data) {
                alert("You have successfully saved this page");
            });
    });
}); 