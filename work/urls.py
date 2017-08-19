from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'list$', views.list_work, name='list_works'),
    url(r'retrieve$', views.retrieve_works, name='retrieve_works'),
    url(r'retrieve_enable$', views.retrieve_enable_works, name='retrieve_enable_works'),
    url(r'audit$', views.audit_work, name='audit_work'),
    url(r'shelve$', views.shelve_work, name='shelve_work'),
    url(r'list_recommend$', views.list_work, name='recommend_works'),
    url(r'add_work_category$', views.add_work_category, name='add_work_category'),
    url(r'save_work_category$', views.save_work_category, name='save_work_category'),
    url(r'add_work_to_category$', views.add_work_to_category, name='add_work_to_category'),
    url(r'save_category_works_order$', views.save_category_works_order, name='save_category_works_order'),
    url(r'sticky_work_to_category$', views.sticky_work_to_category, name='sticky_work_to_category'),
    url(r'remove_work_from_category$', views.remove_work_from_category, name='remove_work_from_category'),
    url(r'list_work_categories$', views.list_work_categories, name='list_work_categories'),
    url(r'manage_category_works$', views.manage_category_works, name='manage_category_works'),
    url(r'manage_work_categories$', views.manage_work_categories, name='manage_work_categories'),
    # url(r'manage_category_works$', views.manage_category_works, name='manage_category_works'),
]
