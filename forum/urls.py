from django.conf.urls import url
from . import views

urlpatterns = [
    # login views
    url(r'^login/$', views.user_login, name='login'),

    # section views
    url(r'^$', views.section_list, name='section_list'),
    url(r'^(?P<section>[-\w]+)/$', views.section_detail, name='section_detail'),

    # topic views
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/$', views.topic_detail, name='topic_detail'),


]