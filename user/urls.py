from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'list$', views.list_users, name='list_users'),
    url(r'retrieve$', views.retrieve_users, name='retrieve_users'),
    url(r'list_pay_journals$', views.list_pay_journals, name='list_pay_journals'),
    url(r'retrieve_pay_journals$', views.retrieve_pay_journals, name='retrieve_pay_journals'),
    url(r'list_consume_journals$', views.list_consume_journals, name='list_consume_journals'),
    url(r'retrieve_consume_journals$', views.retrieve_consume_journals, name='retrieve_consume_journals'),

]
