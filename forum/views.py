from django.shortcuts import get_object_or_404, render
from .models import Section, Topic

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

    return render(request,
                  'forum/topic_detail.html',
                  {'topic': topic})