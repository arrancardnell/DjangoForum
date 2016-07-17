from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import LoginForm
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
                  {'topic': topic,
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