from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add', views.add_template, name='add_template'),
    url(r'save$', views.save_template, name='save_template'),
    url(r'modify$', views.modify_template, name='modify_template'),
    url(r'save_modify_template', views.save_modify_template, name='save_modify_template'),
    url(r'list', views.list_template, name='list_template'),
]
