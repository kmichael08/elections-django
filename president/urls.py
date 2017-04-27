from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polska
    url(r'^$', views.index, name='index'),

    url(r'^login/', views.django_login, name='django_login'),

    url(r'^logout/', views.logout_view, name='logout_view'),

    # ex: /obwód/2608053/upload_pdf
    url(r'^obwód/(?P<name>[ 0-9A-Zążęćńśół_a-z-]+)/upload_pdf/$', views.upload_pdf, name='upload_pdf'),

    # ex: /obwód/2608053/edit_votes
    url(r'^obwód/(?P<name>[ 0-9A-Zążęćńśół_a-z-]+)/edit_votes/$', views.edit_votes, name='edit_votes'),

    url(r'^search/$', views.search, name='search'),

    # ex: /polska/media/obwód_2608053
    url(r'^media/(?P<filename>[ _ążźśęćńłó0-9A-Za-z-]+)/$', views.get_pdf, name='get_pdf'),

    # ex: /polska/powiat/nakielski
    url(r'^(?P<typ>[ 0-9A-Zążęćńśół_a-z-]+)/(?P<name>[ _ążźśęćńłó0-9A-Za-z-]+)/$', views.get_unit, name='get_unit'),

]