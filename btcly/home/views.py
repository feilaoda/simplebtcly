# Create your views here.
import os
from os.path import abspath, dirname
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _


def index(request):
    return TemplateResponse(request, "home/index.html");
