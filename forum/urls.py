from django.conf.urls import url
from . import views

urlpatterns = [
    # section views
    url(r'^$', views.section_list, name='section_list'),
]