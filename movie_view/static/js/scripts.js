var imdbids = []

$(document).ready(function(){
    $('#movie-grid *, header, footer').hide().load().delay(1000).fadeIn(800);

    $('.movie-item').hover(function() {
        $(this).addClass('hover');
    }, function(){
        $(this).removeClass('hover');
    });

    $('.movie-item').mousedown(function() {
        $(this).css('background-color', 'rgba(171, 171, 171, 0.1)');
    }).mouseup(function() {
        $(this).css('background-color', '');
    });
});
