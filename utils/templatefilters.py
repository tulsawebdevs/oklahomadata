import logging
from django.template import Library, Variable, VariableDoesNotExist
logger = logging.getLogger('okdata')

register = Library()

@register.filter
def hash(obj, attr):
    print attr, 'a'
    pseudo_context = { 'object' : obj }
    try:
        value = Variable('object.%s' % attr).resolve(pseudo_context)
    except VariableDoesNotExist:
        value = None
    return value
