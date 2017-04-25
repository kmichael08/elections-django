from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polska
    url(r'^$', views.index, name='index'),

    # ex: /polska/media/obwód_2608053
    url(r'^media/(?P<filename>[ _ążźśęćńłó0-9A-Za-z-]+)/$', views.get_pdf, name='get_pdf'),

    #ex: /polska/powiat/nakielski
    url(r'^(?P<typ>[ 0-9A-Zążęćńśół_a-z-]+)/(?P<name>[ _ążźśęćńłó0-9A-Za-z-]+)/$', views.get_unit, name='get_unit'),

]