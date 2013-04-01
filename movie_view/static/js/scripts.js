var movies = {},
    ALL;

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
        $('.hover').css('background-color', '').removeClass('hover');
    });

    $('.modalimage').click(function() {
        var movieid = $(this).parent().attr('id'),
            title = $(this).parent().find('p').text(),
            tag = movies[movieid].tag,
            imdblink = 'http://www.imdb.com/title/' + movies[movieid].imdb;
        
        $('.modal-header h3').text(title);
        $('#modal-tag').text(tag);
        
        var appletrailersrc = '<source src="'+ movies[movieid].appletrailer +'">';
        var youtubetrailersrc = '<source src="'+ movies[movieid].youtubetrailer +'">';
        $('.modal-trailer').empty().append('<source src="');

        $('#imdblink').attr('href', imdblink);
        console.log(movies[movieid].filename)
        var beamerlink = '/beam/' + title.replace(/ /g, '~');
        $('#beamer').attr('href', beamerlink);
    });
}
