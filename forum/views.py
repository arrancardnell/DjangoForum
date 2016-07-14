from django.shortcuts import get_object_or_404, render
from .models import Section

def section_list(request):
    sections = Section.members.all()
    return render(request,
                  'forum/section_list.html',
                  {'sections': sections})

def section_detail(request, section):
    section = get_object_or_404(Section,
                                title=section)
    return render(request,
                  'forum/section_detail.html',
                  {'section': section})