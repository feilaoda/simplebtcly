# Create your views here.
import os
from os.path import abspath, dirname
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _


def home_resource(request):
    return TemplateResponse(request, "resources/home_resource.html");

def show_resource(request, resource_id):
    filepath = abspath(dirname(__file__)) + "/templates" 
    filename = "resources/upload/%s.html" % (str(resource_id))
    if os.path.exists(filepath+"/"+filename):
        return TemplateResponse(request, filename);
    else:
        return HttpResponseRedirect("/resource/#/resource/%s/" % (str(resource_id)))
        #return TemplateResponse(request, "resources/show_resource.html");
        #raise Http404
      