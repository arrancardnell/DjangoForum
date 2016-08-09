from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def jump_menu(context):
    jump_menu = {}
    request = context['request']
    path = str(request.path)
    path_list = path.split('/')
    
    return path_list[1:-1]