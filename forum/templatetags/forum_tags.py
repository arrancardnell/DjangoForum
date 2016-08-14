from collections import OrderedDict
from django import template
from django.contrib.auth.models import User
from django.db.models import Count, Sum

import datetime

from ..models import Section, Topic, Post

register = template.Library()

@register.assignment_tag
def top_three_posters(count=3):
    today = datetime.date.today()
    top_three_posters = User.objects.filter(
        topic_posts__created__gte=today).annotate(
        posts_today=Count('topic_posts')).order_by('-posts_today', '-username')[:count]
    return top_three_posters

@register.inclusion_tag('forum/jump_menu.html', takes_context=True)
def jump_menu(context):
    # jump_menu = OrderedDict([('jumps', {})])
    # jumps = OrderedDict()
    jump_menu = OrderedDict()
    jump_menu['jumps'] = OrderedDict()
    request = context['request']
    path = str(request.path).strip('/')  # forum/general/welcome
    path_list = path.split('/')  # ['forum', 'general', 'welcome']

    for index, jump_name in enumerate(path_list):
        link = '/' + '/'.join(path_list[:index + 1]) + '/'   # /forum/general/welcome/
        title = None

        if index == 1:  # sections will be at index 1
            title = Section.objects.filter(slug__exact=jump_name).values_list('title', flat=True)
        if index == 2:  # topics will be at index 2
            title = Topic.objects.filter(slug__exact=jump_name).values_list('title', flat=True)

        if title:
            jump_menu['jumps'][title[0]] = link
        else:
            jump_menu['jumps'][jump_name.replace('-', ' ')] = link

        if index == len(path_list)-1:
            jump_menu['final_jump'] = link

    return jump_menu