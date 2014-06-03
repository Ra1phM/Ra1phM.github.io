function checkWidth(init) {
    var w = 768; // 990
    if ($(window).width() >= w ) {
        $('#sidebar').removeClass('sidebar-push-right');
        $('#content').removeClass('content-push-right');
        $('#showLeftPush span').removeClass('glyphicon-chevron-left');
        $('#showLeftPush span').addClass('glyphicon-chevron-right');
    }
};

$(document).ready(function() {
    var showLeftPush = document.getElementById('showLeftPush');
    showLeftPush.onclick = function() {
        $('#sidebar').toggleClass('sidebar-push-right');
        $('#content').toggleClass('content-push-right');
        $('#showLeftPush span').toggleClass('glyphicon-chevron-left');
        $('#showLeftPush span').toggleClass('glyphicon-chevron-right');
    };

    $(window).resize(function() {
        checkWidth(false);
    });
});