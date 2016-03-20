$(function() {
    $("input:file[id=uploadBtn]").change (function() {

        $("#uploadFile").val($(this).val());
        $("span.uploadBtn").text("upload");
    });
});
