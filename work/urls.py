from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'list$', views.list_work, name='list_works'),
    url(r'retrieve', views.retrieve_works, name='retrieve_works'),
    url(r'audit', views.audit_work, name='audit_work'),
    url(r'shelve', views.shelve_work, name='shelve_work'),
    url(r'list_recommend', views.list_work, name='recommend_works'),
]
