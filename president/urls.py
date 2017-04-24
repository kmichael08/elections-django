from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polska
    url(r'^$', views.index, name='index'),

    #ex: /powiat/nakielski
    url(r'^(?P<typ>[ 0-9A-Zążęćńśóła-z-]+)/(?P<name>[ ążźśęćńłó0-9A-Za-z-]+)/$', views.get_unit, name='get_unit'),

]