from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

def index(request):
    context = RequestContext(request, {'settings': settings})

    try:
        address = request.REQUEST.get('address')
        context['address'] = address
    except KeyError:
        pass

    return render_to_response('boundary_demo/index.html', context)
