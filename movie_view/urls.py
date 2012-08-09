from django.conf.urls import patterns, include, url
from movie_view.views import home, movie

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        ('^/$', home.greet),
        ('^movie/(.*)/$', movie.show),
    # Examples:
    # url(r'^$', 'movie_view.views.home', name='home'),
    # url(r'^movie_view/', include('movie_view.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
