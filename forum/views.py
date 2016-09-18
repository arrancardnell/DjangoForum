from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from .forms import AddPostForm, AddTopicForm, LoginForm, PrivateConversationForm, PrivateMessageForm,\
    ProfileEditForm, UserEditForm, UserRegistrationForm
from .models import Section, Topic, Post, Profile, Message

import json
import redis

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

# section views
def section_list(request):
    sections = Section.members.all()
    return render(request,
                  'forum/section_list.html',
                  {'sections': sections})


def section_detail(request, section):
    section = get_object_or_404(Section,
                                slug=section)
    # annotate each topic with its latest post and order the topics
    # by most recent post
    topic_list = Topic.objects.filter(
        section=section).annotate(
        latest_post=Max(
            'topic_posts__created')).order_by('-latest_post')
    paginator = Paginator(topic_list, 5)
    page = request.GET.get('page')
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer then deliver the first page
        topics = paginator.page(1)
    except EmptyPage:
        # If page is out of range then deliver the last page
        topics = paginator.page(paginator.num_pages)

    return render(request,
                  'forum/section_detail.html',
                  {'section': section,
                   'page': page,
                   'topics': topics})


# topic views
def topic_detail(request, section, topic):
    section = get_object_or_404(Section,
                                slug=section)
    topic = get_object_or_404(Topic,
                              section=section,
                              slug=topic)
    # increment the total views by 1
    r.incr('topic:{}:views'.format(topic.id))
    post_list = Post.objects.filter(topic=topic)
    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer then deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range then deliver the last page
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'forum/topic_detail.html',
                  {'section': section,
                   'topic': topic,
                   'page': page,
                   'posts': posts})


@login_required
def add_topic(request, section):
    if request.method == 'POST':
        topic_form = AddTopicForm(request.POST)
        post_form = AddPostForm(request.POST)
        if topic_form.is_valid() and post_form.is_valid():
            cd_topic_form = topic_form.cleaned_data
            cd_post_form = post_form.cleaned_data

            # assign user and section to new topic
            new_topic = topic_form.save(commit=False)
            new_post = post_form.save(commit=False)

            topic_section = get_object_or_404(Section,
                                              slug=section)
            new_topic.owner = request.user
            new_topic.section = topic_section
            new_topic.save()

            # assign user and topic to opening post
            new_post.owner = request.user
            new_post.topic = new_topic
            new_post.save()

            return redirect('forum:section_detail', section)
    else:
        topic_form = AddTopicForm
        post_form = AddPostForm

    return render(request, 'forum/add_topic.html',
                  {'topic_form': topic_form,
                   'post_form': post_form})


# registration views
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but don't save
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the user
            new_user.save()
            # create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

# inbox views
@login_required
def new_conversation(request):
    if request.method == 'POST':
        private_conversation_form = PrivateConversationForm(request.POST)
        private_message_form = PrivateMessageForm(request.POST)

        if private_conversation_form.is_valid() and private_message_form.is_valid():
            # create new conversation
            new_private_conversation = private_conversation_form.save(commit=False)
            # assign a recipient
            new_private_conversation(owner=request.user,
                                     recipient=private_conversation_form.cleaned_data['recipient'],
                                     title=private_conversation_form.cleaned_data['title'])
            # save the form
            new_private_conversation.save()

            # add the new private message to the form
            new_private_message = private_message_form.save(commit=False)
            # link the message to the form
            new_private_message(sender=request.user,
                                conversation=new_private_conversation,
                                content=private_message_form.cleaned_data['content'])
            # save the message
            new_private_message.save()
            return redirect('forum:inbox')
    else:
        private_conversation_form = PrivateConversationForm
        private_message_form = PrivateMessageForm
    return render(request,
                  'forum/new_conversation.html',
                  {'private_conversation_form': private_conversation_form,
                   'private_message_form': private_message_form})

# login views
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# post views
@login_required
def add_post(request, section, topic):
    if request.method == 'POST':
        form = AddPostForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_post = form.save(commit=False)

            # assign current user and topic to post
            post_section = get_object_or_404(Section,
                                             slug=section)
            post_topic = get_object_or_404(Topic,
                                           section=post_section,
                                           slug=topic)

            new_post.owner = request.user
            new_post.topic = post_topic

            # save the post
            new_post.save()

            return redirect('forum:topic_detail', section, topic)
    else:
        form = AddPostForm

    return render(request,
                  'forum/add_post.html',
                  {'form': form})

def update_likes(request):

    if request.method == 'POST':
        response_data = {}
        post_id = request.POST.get('post_id')
        post_action = request.POST.get('post_action')

        post = Post.objects.get(id=post_id)
        user = request.user
        if post.owner != user:

            if post_action == 'like':
                post.likes.add(user)
            else:
                post.likes.remove(user)
            post.save()

            response_data['result'] = 'updated'
            response_data['post_id'] = post.pk
            response_data['users_like'] = list(post.likes.all().values_list('username', flat=True))
            response_data['post_likes'] = post.likes.count()

            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        else:
            return HttpResponse({'result': 'not updated'},
                                content_type='application/json')
    else:
        return HttpResponse({'result': 'not updated'},
                            content_type='application/json')
# chat views
def add_chat_message(request):

    if request.method == 'POST':
        message_text = request.POST.get('chat_message_text')
        if message_text:
            user = request.user
            response_data = {}

            new_message = Message.objects.create(content=message_text,
                                                 owner=user)
            new_message.save()

            response_data['result'] = 'created'
            response_data['message_pk'] = new_message.pk
            response_data['text'] = new_message.content
            response_data['created'] = new_message.created.strftime('%b %d, %Y %I:%M %p')
            response_data['owner'] = new_message.owner.username

            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': 'not created'}),
                                content_type='application/json')
    else:
        return HttpResponse(json.dumps({'result': 'not created'}),
                            content_type='application/json')

def refresh_chat(request):

    if request.method == 'POST':

        last_message = Message.objects.latest('created').content
        last_chat_message = request.POST.get('last_message')

        # check whether any new chat messages have been added
        if last_message != last_chat_message:
            response_data = {}

            # display the last five chat messages only
            messages = Message.objects.all()
            # need to convert to a list to use negative indexing
            last_ten_messages = list(messages.values('owner__username', 'created', 'content'))[-10:]
            last_ten_messages.reverse()
            for idx, message in enumerate(last_ten_messages):
                last_ten_messages[idx]['created'] = message['created'].strftime('%b %d, %Y %I:%M %p')

            response_data['result'] = 'refreshed'
            response_data['messages'] = last_ten_messages

            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'result': 'not refreshed'}),
                                content_type='application/json')
    else:
        return HttpResponse(json.dumps({'result': 'not refreshed'}),
                            content_type='application/json')

# profile views
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 date=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       date=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'forum/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})