$(document).ready(function(){
    // dropdown search
    $(".dropdown-toggle").click(function() {
        $(".dropdown-menu").toggle();
        $('.nav-input').focus();
    });

    // dropdown menu
    $("#icon-toggle").click(function (){
        $(".sidebar-links").toggle();
    })

    // Text area autosize
    $("textarea").on("keyup", function(e) {
        var scHeight = $(this)[0].scrollHeight;
    });
});

