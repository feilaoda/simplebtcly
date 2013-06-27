from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'btcly.home.views.index', name='home'),
)
