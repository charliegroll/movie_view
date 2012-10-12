var imdbids = [];
var appletrailers = [];
var youtubetrailers = [];
var ALL;

$(document).ready(function(){
    ALL = $('.movie-item');

    wrapyourtool();
    bindings();

    $('#movie-grid *, header, footer').hide().load().delay(1000).fadeIn(800);

    $('.movie-item').mousedown(function() {
        $(this).css('background-color', 'rgba(171, 171, 171, 0.1)');
    }).mouseup(function() {
        $(this).css('background-color', '');
    });

    $('.search-query').on('keyup', function() {
        var key = $(this).val().toLowerCase();
        $('#movie-grid').empty();
        ALL.each(function() {
            var text = $(this).find('p').text().toLowerCase();
            if (text.indexOf(key) >= 0) {
                $('#movie-grid').append($(this));
            }
        });
        wrapyourtool();
        bindings();
    });
});

function wrapyourtool() {
    var wrapper = '<div class="movie-row row-fluid"></div>';
    $('.movie-item:nth-child(6n)').each(function() {
        $(this).prevAll('.movie-item').andSelf().wrapAll(wrapper);
    });
    $('#movie-grid>.movie-item').wrapAll(wrapper);
}

function bindings() {
    $('.movie-item').hover(function() { //these get removed when filtering in search bar
        $(this).addClass('hover');
    }, function(){
        $(this).removeClass('hover');
    });

    $('.modalimage').click(function() {
        var movieid = $(this).parent().attr('id');
        var title = $(this).parent().find('p').text();
        $('#moviemodal h3').text(title);
        
        var appletrailersrc = '<source src="'+ appletrailers[movieid] +'">';
        var youtubetrailersrc = '<source src="'+ youtubetrailers[movieid] +'">';
        $('.modal-trailer').empty().append('<source src="');

        var imdblink = 'http://www.imdb.com/title/' + imdbids[movieid];
        $('.modal-body>ul').empty().append('<li><a href="'+ imdblink +'" target="_blank">IMDb</a></li>');
    });
}
