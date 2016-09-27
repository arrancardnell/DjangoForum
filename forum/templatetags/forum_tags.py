from collections import OrderedDict
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.backends import locmem
from django.db.models import Count, Max

from forum.models import Section, Topic, Post, Message
from inbox.models import PrivateConversation

import datetime
import redis

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.all().count()

@register.simple_tag
def total_members():
    return User.objects.all().count()

@register.simple_tag
def newest_member():
    return User.objects.latest('date_joined')

@register.simple_tag
def total_views(topic_id):
    return r.get('topic:{}:views'.format(topic_id))

@register.assignment_tag
def online_members():
    users = list(User.objects.all().values_list('username', flat=True))
    seen_users = cache.get_many(['seen_{}'.format(user) for user in users])
    online_members = []
    # check that the user has had activity in the time limit set by USER_ONLINE_TIMEOUT
    for user in seen_users:
        if seen_users[user] + datetime.timedelta(
                seconds=settings.USER_ONLINE_TIMEOUT) > datetime.datetime.now():
            online_members.append(user.split('_', 1)[1])
    return sorted(online_members)

@register.assignment_tag
def top_three_posters(count=3):
    today = datetime.date.today()
    # annotate each each user with their post count for today and order them
    top_three_posters = User.objects.filter(
        topic_posts__created__gte=today).annotate(
        posts_today=Count('topic_posts')).order_by('-posts_today', '-username')[:count]
    return top_three_posters

@register.assignment_tag
def top_three_topics(count=3):
    # annotate each topic with its total posts and the latest post. Filter any topic
    # with less than 5 posts (can't be a hot topic if noone is posting!), order them
    # by the time of last post and return the top three topicd
    top_three_topics = Topic.objects.annotate(
        total_posts=Count('topic_posts'), latest_post=Max('topic_posts__created')).filter(
        total_posts__gte=5).order_by('-latest_post', '-total_posts')[:3]
    return top_three_topics

@register.inclusion_tag('forum/jump_menu.html', takes_context=True)
def jump_menu(context):
    jump_menu = OrderedDict()
    jump_menu['jumps'] = OrderedDict()
    request = context['request']
    path = str(request.path).strip('/')  # forum/general/welcome
    path_list = path.split('/')  # ['forum', 'general', 'welcome']

    for index, jump_name in enumerate(path_list):
        link = '/' + '/'.join(path_list[:index + 1]) + '/'   # /forum/general/welcome/
        title = None

        if index == 1:
            # convert conversation id to title
            if 'inbox' in path_list:
                title = PrivateConversation.objects.filter(id=jump_name).values_list('title', flat=True)
            else:  # sections will be at index 1
                title = Section.objects.filter(slug__exact=jump_name).values_list('title', flat=True)
        if index == 2:  # topics will be at index 2
            title = Topic.objects.filter(slug__exact=jump_name).values_list('title', flat=True)

        if title:
            jump_menu['jumps'][title[0]] = link
        else:
            jump_menu['jumps'][jump_name.replace('-', ' ').replace('_', ' ')] = link

    return jump_menu

@register.inclusion_tag('forum/chat_box.html', takes_context=True)
def chat_messages(context):
    # display the last five chat messages only
    messages = Message.objects.all()
    # need to convert to a list to use negative indexing
    last_ten_messages = list(messages.values('owner__username', 'created', 'content'))[-10:]
    last_ten_messages.reverse()  # newest messages at the top of the chat
    request = context['request']
    authenticated = request.user.is_authenticated()  # check if user is logged in
    path = request.path
    return {'last_ten_messages': last_ten_messages,
            'authenticated': authenticated,
            'path': path}