from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect

from .forms import LoginForm, AddPostForm
from .models import Section, Topic, Post

# section views
def section_list(request):
    sections = Section.members.all()
    return render(request,
                  'forum/section_list.html',
                  {'sections': sections})

def section_detail(request, section):
    section = get_object_or_404(Section,
                                slug=section)
    topics = Topic.objects.filter(section=section)

    return render(request,
                  'forum/section_detail.html',
                  {'section': section,
                   'topics': topics})

# topic views
def topic_detail(request, section, topic):
    section = get_object_or_404(Section,
                                slug=section)
    topic = get_object_or_404(Topic,
                              section=section,
                              slug=topic)
    posts = Post.objects.filter(topic=topic)

    return render(request,
                  'forum/topic_detail.html',
                  {'section': section,
                   'topic': topic,
                   'posts': posts})

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