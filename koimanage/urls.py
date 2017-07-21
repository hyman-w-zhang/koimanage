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
from . import views

urlpatterns = [
    url(r'^$', view=views.admin_home, name='admin_home'),
    url(r'^accounts/', admin.site.urls),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'template/', include(template_urls)),
    url(r'work/', include(work_urls)),
    url(r'^version/add', view=views.add_version, name='add_version'),
    url(r'^version/list', view=views.retrieve_versions, name='list_version'),
    url(r'^version/save', view=views.save_version, name='save_version'),
    url(r'^version/delete/([\w\-]+)', view=views.delete_version, name='delete_version'),
]
