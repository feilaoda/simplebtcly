from django.conf.urls import patterns, url




urlpatterns = patterns('btcly.resources.views',
    url(r'^$', 'home_resource', name='home-resource'),   

    url(r'^(?P<resource_id>\w*)/$', 'show_resource', name='show-resource'),    
)
