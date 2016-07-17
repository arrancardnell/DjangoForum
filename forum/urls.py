from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # login views
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$',
        auth_views.logout_then_login, name='logout_then_login'),

    # password views
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

    # section views
    url(r'^$', views.section_list, name='section_list'),
    url(r'^(?P<section>[-\w]+)/$', views.section_detail, name='section_detail'),

    # topic views
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/$', views.topic_detail, name='topic_detail'),

    # post views
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/add_post/$', views.add_post, name='add_post'),

]