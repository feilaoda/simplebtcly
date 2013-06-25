from django.db import models
from django.db.models.query import QuerySet
from django.core import serializers
import json


def model_to_json(obj):
   if isinstance(obj, QuerySet):
       return json.dumps(obj, cls=DjangoJSONEncoder)
   if isinstance(obj, models.Model):
       #do the same as above by making it a queryset first
       set_obj = [obj]
       list_obj = json.loads(serializers.serialize('json', set_obj))
       if len(list_obj) <=0:
            return "{}"
       set_str = json.dumps(list_obj[0])
       
       #eliminate brackets in the beginning and the end 
       str_obj = set_str 
   return str_obj


