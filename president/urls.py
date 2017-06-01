from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polska
    url(r'^$', views.index, name='index'),

    url(r'^login/', views.django_login, name='django_login'),

    url(r'^logout/', views.logout_view, name='logout_view'),

    # ex: /polska/obwód/2608053/upload_pdf
    url(r'^obwód/(?P<name>[ 0-9A-ZążęćńśółŁĆŚÓŻ_a-z-]+)/upload_pdf/$', views.upload_pdf, name='upload_pdf'),


    url(r'^search/$', views.search, name='search'),

    # ex: /polska/edit_votes/2608053
    url(r'^edit_votes_dynamic/(?P<name>[ 0-9A-ZążęćńśółŁĆŚÓŻ_a-z-]+)/$', views.edit_votes_dynamic, name='edit_votes_dynamic'),

    url(r'^lista_gmin/$', views.lista_gmin, name='lista_gmin'),

    # ex: /polska/media/obwód_2608053
    url(r'^media/(?P<filename>[ _ążźśęćńłóŁĆŚÓŻ0-9A-Za-z-]+)/$', views.get_pdf, name='get_pdf'),

    # ex: /polska/powiat/nakielski
    url(r'^(?P<typ>[ 0-9A-Zążęćńśół_a-z-]+)/(?P<name>[ _ążźśęćńłóŁĆÓŚŻ0-9A-Za-z-]+)/$', views.get_unit, name='get_unit'),

    # ex: /polska/data/powiat/nakielski
    url(r'^data/(?P<typ>[ 0-9A-Zążęćńśół_a-z-]+)/(?P<name>[ _ążźśęćńłóŁĆŚÓŻ0-9A-Za-z-]+)/$', views.get_unit_data, name='get_unit_data'),


]