from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<id>[0-9]+)/delete$', views.delete, name='delete'),
    url(r'^clients/$', views.client_list, name='client_list'),
    url(r'^rooms/$', views.room_list, name='room_list'),
    url(r'^hotels/$', views.hotel_list, name='hotel_list'),
    url(r'^clients/xml/$', views.client_xml_fill, name='client_xml_fill'),
    url(r'^rooms/xml/$', views.room_xml_fill, name='room_xml_fill'),
    url(r'^hotels/xml/$', views.hotel_xml_fill, name='hotel_xml_fill')
]
