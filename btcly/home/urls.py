from django.conf.urls import patterns, url




urlpatterns = patterns('btcly.home.views',
    url(r'^$', 'home_resource', name='home-resource'),   

    url(r'^(?P<resource_id>\d*)/$', 'show_resource', name='show-resource'),    
)
