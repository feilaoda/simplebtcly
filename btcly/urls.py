from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^resource/', include('btcly.resources.urls', namespace='resources')),
    url(r'', include('btcly.core.urls', namespace='core')),
)

urlpatterns += patterns('',
(r'^static/(?P.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

#urlpatterns += patterns('', url(r'^static/(?P.*)$', 
#    'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),) 

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#urlpatterns += staticfiles_urlpatterns()