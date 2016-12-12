from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^clients/$', views.clients_list, name='clients_list'),
    # url(r'^clients/new', views.clients_post, name='clients_post'),
    # url(r'^clients/(?P<id>[0-9]+)/$', views.clients_get, name='clients_get'),
    # url(r'^clients/(?P<id>[0-9]+)/update/$', views.clients_update, name='clients_update'),
    # url(r'^clients/(?P<id>[0-9]+)/delete/$', views.clients_delete, name='clients_delete'),
    # url(r'^hotels/(?P<id>[0-9]+)/$', views.hotels_get, name='hotels_get'),
    # url(r'^hotels/(?P<id>[0-9]+)/update/$', views.hotels_update, name='hotels_update'),
    # url(r'^hotels/new', views.hotels_post, name='hotels_post')
    # url(r'^hotels/(?P<id>[0-9]+)/delete/$', views.hotels_delete, name='hotels_delete')
]
