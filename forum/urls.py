from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # ajax_views
    url(r'ajax/add_chat_message/$', views.add_chat_message, name='add_chat_message'),
    url(r'ajax/refresh_chat/$', views.refresh_chat, name='refresh_chat'),
    url(r'ajax/update_likes/$', views.update_likes, name='update_likes'),

    # login views
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^logout-then-login/$',
        auth_views.logout_then_login, name='logout_then_login'),

    # edit views
    url(r'^edit/$', views.edit, name='edit'),

    # register views
    url(r'^register/$', views.register, name='register'),

    # password views
    url(r'^password-change/$', auth_views.password_change, name='password_change'),
    url(r'^password-change/done/$', auth_views.password_change_done, name='password_change_done'),

    # reset password
    url(r'^password-reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+/$)',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # private message views
    url(r'^inbox/$', views.inbox, name='inbox'),

    # section views
    url(r'^$', views.section_list, name='section_list'),
    url(r'^(?P<section>[-\w]+)/$', views.section_detail, name='section_detail'),

    # topic views
    url(r'^(?P<section>[-\w]+)/add_topic/$', views.add_topic, name='add_topic'),
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/$', views.topic_detail, name='topic_detail'),

    # post views
    url(r'^(?P<section>[-\w]+)/(?P<topic>[-\w]+)/add_post/$', views.add_post, name='add_post'),

]