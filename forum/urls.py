from django.conf.urls import url
from . import views

urlpatterns = [
    # section views
    url(r'^$', views.section_list, name='section_list'),
    url(r'(?P<section>[-\w]+)/$', views.section_detail, name='section_detail'),
]