from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'add$', views.add_template, name='add_template'),
    url(r'save$', views.save_template, name='save_template'),
    url(r'modify$', views.modify_template, name='modify_template'),
    url(r'save_modify_template$', views.save_modify_template, name='save_modify_template'),
    url(r'list$', views.list_template, name='list_template'),

    url(r'add_template_category$', views.add_template_category, name='add_template_category'),
    url(r'save_template_category$', views.save_template_category, name='save_template_category'),
    url(r'list_template_categories$', views.list_template_categories, name='list_template_categories'),
    url(r'add_template_to_category$', views.add_template_to_category, name='add_template_to_category'),
    url(r'save_category_templates_order$', views.save_category_templates_order, name='save_category_templates_order'),
    url(r'sticky_template_to_category$', views.sticky_template_to_category, name='sticky_template_to_category'),
    url(r'remove_template_from_category$', views.remove_template_from_category, name='remove_template_from_category'),
    url(r'manage_category_templates$', views.manage_category_templates, name='manage_category_templates'),
]
