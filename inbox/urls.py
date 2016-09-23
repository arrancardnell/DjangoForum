from django.conf.urls import url

from inbox import views

urlpatterns = [

    # private message views
    url(r'^$', views.inbox, name='inbox'),
    url(r'^compose-message/$', views.new_conversation, name='compose_message'),
    url(r'^(?P<conversation_id>[-\w]+)/$', views.view_conversation, name='view_conversation'),
]