from collections import OrderedDict
from django import template

register = template.Library()


@register.inclusion_tag('forum/jump_menu.html', takes_context=True)
def jump_menu(context):
    jump_menu = OrderedDict([('jumps', {})])
    jumps = OrderedDict()
    request = context['request']
    path = str(request.path).strip('/')  # forum/general/welcome
    path_list = path.split('/')  # ['forum', 'general', 'welcome']

    for index, jump_name in enumerate(path_list):
        link = '/' + '/'.join(path_list[:index + 1]) + '/'   # /forum/general/welcome/
        jumps.setdefault(jump_name, link)
    jump_menu['jumps'].update(jumps)

    return jump_menu