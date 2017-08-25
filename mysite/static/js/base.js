$(document).ready(function(){
    $("#commentForm").hide();

    $("#searchTitles").autocomplete( "/api/get_books/");  
    
    // http://forum.jquery.com/topic/jquery-autocomplete-submit-form-on-result
    $("#searchTitles").result(function (event, data, formatted) {
        $("#searchProgress").append('<img src="img/loader.gif" alt="Loading ..." id="loading" />');
            var searchVal = $("#searchTitles").val();
            $("#searchTitles").val('');
            
            if(formatted.indexOf("notSelectRow") != -1) {    
                $("#loading").hide();
            } else {
                var bookid = formatted.replace(/.*id="([^"]+)".*/gi, "$1");
                location.href= "/books/" + bookid;                
            }
    });

    // http://www.dailycoding.com/Posts/default_text_fields_using_simple_jquery_trick.aspx
    $(".defaultText").focus(function(srcc){
        if ($(this).val() == $(this)[0].title){
            $(this).removeClass("defaultTextActive");
            $(this).val("");
        }
    });

    $(".defaultText").blur(function(){
        if ($(this).val() == ""){
            $(this).addClass("defaultTextActive");
            $(this).val($(this)[0].title);
        }
    });

    $(".defaultText").blur();
});
