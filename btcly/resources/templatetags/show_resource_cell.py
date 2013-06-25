from django.template.loader import render_to_string
from django.template import Library
from django.template import RequestContext
from django.http import  Http404


register = Library()


@register.simple_tag
def show_resource_cell(request, resource_id):
    
    category = pin.entity.category
    template_file = 'entities/templatetags/show_entity_%s.html' % (category)
    return render_to_string(template_file,
        {'pin': pin, 'entity': pin.entity},
        context_instance=RequestContext(request))
