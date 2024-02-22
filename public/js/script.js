$(document).ready(function(){
    // side bar toggle
    $('#icon-toggle').click(function(){
        var sidebar = $('.sidebar-links');
        var iconOpen = $('#icon-open');
        var iconToggle = $('#icon-toggle');
        if (sidebar.css('display') === 'none') {
            sidebar.fadeIn(200);
            iconOpen.fadeOut(100, function() {
                iconToggle.html('<i class="fa-solid fa-xmark fa-xl"></i>');
            });
        } else {
            sidebar.fadeOut(200);
            iconToggle.html('<i class="fas fa-bars fa-xl" id="icon-open"></i>');
        }
    });

    // dropdown search
    $(".dropdown-toggle").click(function() {
        $(".dropdown-menu").toggle();
        $('.nav-input').focus();
    });
});