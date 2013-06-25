from django.conf.urls import patterns, include, url
from tastypie.api import Api

# from .api import PinResource
# from .api import UserResource


# pin_resource = PinResource()
# user_resource = UserResource()

# api = Api(api_name='v1')
# api.register(PinResource(), canonical=True)
# api.register(UserResource(), canonical=True)

# urlpatterns = patterns('',
#     url(r'', include(pin_resource.urls)),
#     url(r'', include(user_resource.urls)),
# )

# urlpatterns = patterns('', 
#     url(r'', include(api.urls)),
# )


from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from .api import PinHandler, SinglePinHandler, UserHandler

auth = HttpBasicAuthentication(realm="domain.com")
# ad = { 'authentication': auth }
ad = {}

pin_resource = Resource(handler=PinHandler, **ad)
single_pin_resource = Resource(handler=SinglePinHandler, **ad)
# user_resource = Resource(handler=UserHandler, **ad)

urlpatterns = patterns('',
    
    # url(r'^v1/pin/(?P<id>[^/]+)/$', single_pin_resource), 
    url(r'^v1/pin/$', pin_resource), 
    # url(r'^user/(?P<user_id>[^/]+)/$', user_resource), 
)
