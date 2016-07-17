from django.conf.urls import url
from . import views

urlpatterns = [
    # login views
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^logout-then-login/$',
        'django.contrib.auth.views.logout_then_login', name='logout_then_login'),

    # section views
    url(r'^$', views.section_list, name='section_list'),
    url(r'^(?P<section>[-\w]+)/$', views.section_detail, name='section_detail'),

    # topic views
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/$', views.topic_detail, name='topic_detail'),


]