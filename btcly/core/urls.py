from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'btcly.home.views.index', name='home'),
    url(r'^private/$', 'btcly.core.views.private', name='private'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'}, name='login'),
    url(r'^register/$', 'btcly.core.views.register', name='register'),
    url(r'^logout/$', 'btcly.core.views.logout_user', name='logout'),
)
