from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization

from django.contrib.auth.models import User

from pinkup.boards.models import Board
from pinkup.pins.models import Pin
from pinkup.entities.models import Entity

# class UserResource(ModelResource):
#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'user'
#         excludes = ['email', 'password', 'is_superuser']
#         # Add it here.
#         authentication = BasicAuthentication()
#         authorization = DjangoAuthorization()
#         fields = ['username', 'is_active']


# class BoardResource(ModelResource):  # pylint: disable-msg=R0904
#     user = fields.ForeignKey(UserResource, 'user')

#     class Meta:
#         queryset = Pin.objects.all()
#         resource_name = 'board'
#         include_resource_uri = False
#         filtering = {
#             'created': ['gt'],
#         }

#     def build_filters(self, filters=None):
#         if filters is None:
#             filters = {}

#         orm_filters = super(BoardResource, self).build_filters(filters)

#         if 'tag' in filters:
#             orm_filters['tags__name__in'] = filters['tag'].split(',')

#         return orm_filters

#     def dehydrate_tags(self, bundle):
#         return map(str, bundle.obj.tags.all())

#     def save_m2m(self, bundle):
#         tags = bundle.data.get('tags', [])
#         bundle.obj.tags.set(*tags)
#         return super(BoardResource, self).save_m2m(bundle)






# class PinResource(ModelResource):  # pylint: disable-msg=R0904
#     #user = fields.ForeignKey(UserResource, 'submitter')
#     tags = fields.ListField()

#     class Meta:
#         queryset = Entity.objects.all()
#         resource_name = 'pin'
#         include_resource_uri = False
#         filtering = {
#             'published': ['gt'],
#         }

#     def build_filters(self, filters=None):
#         if filters is None:
#             filters = {}

#         orm_filters = super(PinResource, self).build_filters(filters)
        
#         # if 'user' in filters:
#         #     orm_filters['user__id'] = filters['user']
#         # else:

#         #     orm_filters['user__id'] = 0
#         #     return orm_filters

#         if 'tag' in filters:
#             orm_filters['tags__name__in'] = filters['tag'].split(',')

#         return orm_filters

#     def dehydrate_tags(self, bundle):
#         return map(str, bundle.obj.tags.all())

#     def save_m2m(self, bundle):
#         tags = bundle.data.get('tags', [])
#         bundle.obj.tags.set(*tags)
#         return super(PinResource, self).save_m2m(bundle)


import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from django.core.urlresolvers import reverse
from pinkup.pins.models import Pin


paging_offset = 'offset'
paging_limit = 'limit'
limit_default = 30
limit_max = 200



class PinHandler(BaseHandler):
    model = Entity
    allowed_methods = ('GET')
    fields = ('id', 'pin_link', 'url', 'title', 'description', 'image', 'thumbnail', ('tags', ('name',)), ('board', ('title',)), ('user', ('username',)) ,'published')
    #exclude = ('id')
    @classmethod
    def pin_link(cls, model):
        try:
            pin = Pin.objects.get(entity_id=model.id,user_id=model.user.id, board_id=model.board.id)
            return reverse("pins:show-pin", kwargs={'pin_id':pin.id})
        except Pin.DoesNotExist:
            return reverse("entities:redirect", kwargs={'entity_id':model.id})

    def read(self, request):
        offset = 0
        try: 
            offset = int(request.GET.get(paging_offset))
        except (ValueError, TypeError): 
            offset = 0

        limit = limit_default
        try: 
            limit = int(request.GET.get(paging_limit))
        except (ValueError, TypeError): 
            limit = limit_default
        if offset < 0:
            offset = 0
        if limit > limit_max:
            limit = limit_max

        try:
            return Entity.objects.all()[offset:offset+limit]
            
        except Entity.DoesNotExist:
            resp = rc.NOT_FOUND            
            return resp

class SinglePinHandler(BaseHandler):
    model = Pin
    allowed_methods = ('GET')
    fields = ('url', 'description', 'image', 'thumbnail', ('board', ('title',)), ('user', ('username',)) ,'published')
    exclude = ('id')

    # def read(self, request, id=None):
    #     try:
    #         base = Pin.objects
    #         if id is None or id == '':
    #             return base.get(id=id)
    #         else:
    #             return base.all()
    #     except Pin.DoesNotExist:
    #         resp = rc.CREATED            
    #         return resp

class UserHandler(BaseHandler):        
    pass