from django.conf.urls import url

from inbox import views

urlpatterns = [

    # private message views
    url(r'^inbox/$', views.inbox, name='inbox'),
    url(r'^compose-message/$', views.new_conversation, name='compose_message'),

]