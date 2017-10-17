"""koimanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from template import urls as template_urls
from work import urls as work_urls
from user import urls as user_urls
from . import views

urlpatterns = [
    url(r'^$', view=views.admin_home, name='admin_home'),
    url(r'^accounts/', admin.site.urls),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'template/', include(template_urls)),
    url(r'work/', include(work_urls)),
    url(r'user/', include(user_urls)),

    url(r'^version/add', view=views.add_version, name='add_version'),
    url(r'^version/list', view=views.retrieve_versions, name='list_version'),
    url(r'^version/save', view=views.save_version, name='save_version'),
    url(r'^version/delete/([\w\-]+)', view=views.delete_version, name='delete_version'),

    url(r'^api_config/add', view=views.add_api_config, name='add_api_config'),
    url(r'^api_config/list', view=views.retrieve_api_configs, name='list_api_config'),
    url(r'^api_config/save$', view=views.save_api_config, name='save_api_config'),
    url(r'^api_config/save_modified', view=views.save_modified_api_config, name='save_modified_api_config'),
    url(r'^api_config/modify/([\w\-]+)', view=views.modify_api_config, name='modify_api_config'),
    url(r'^api_config/delete/([\w\-]+)', view=views.delete_api_config, name='delete_api_config'),

    url(r'^merchandise/add', view=views.add_merchandise, name='add_merchandise'),
    url(r'^merchandise/list', view=views.list_merchandise, name='list_merchandise'),
    url(r'^merchandise/retrieve', view=views.retrieve_merchandises, name='retrieve_merchandises'),
    url(r'^merchandise/save$', view=views.save_merchandise, name='save_merchandise'),
    url(r'^merchandise/disable/([\w\-]+)', view=views.disable_merchandise, name='disable_merchandise'),

    url(r'^comment/list', view=views.list_comments, name='list_comments'),
    url(r'^comment/retrieve', view=views.retrieve_comments, name='retrieve_comments'),
    url(r'^comment/delete', view=views.delete_comment, name='delete_comment'),

    url(r'^banner/add', view=views.add_banner, name='add_banner'),
    url(r'^banner/list', view=views.list_banner, name='list_banner'),
    url(r'^banner/save$', view=views.save_banner, name='save_banner'),
    url(r'^banner/save_banners_order$', view=views.save_banners_order, name='save_banners_order'),
    url(r'^banner/disable', view=views.disable_banner, name='disable_banner'),

    url(r'^index_ad/list', view=views.retrieve_index_ads, name='list_index_ad'),
    url(r'^index_ad/save_modified', view=views.save_modified_index_ad, name='save_modified_index_ad'),
    url(r'^index_ad/modify/([\w\-]+)', view=views.modify_index_ad, name='modify_index_ad'),

    url(r'^activity/list', view=views.retrieve_activities, name='list_activity'),
    url(r'^activity/save_modified', view=views.save_modified_activity, name='save_modified_activity'),
    url(r'^activity/modify/([\w\-]+)', view=views.modify_activity, name='modify_activity'),

]
