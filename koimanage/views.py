from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from . import versions


@login_required
def admin_home(request):
    return render(request, 'base.html')


@login_required
def add_version(request):
    return render(request, 'add_version.html', {'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})


@login_required
def save_version(request):
    code = request.POST['code']
    platform = request.POST['platform']
    name = request.POST['name']
    versions.modify_by_platform_and_name(platform=platform, code=code, name=name)
    return HttpResponseRedirect('/version/list')


@login_required
def retrieve_versions(request):
    return render(request, 'list_version.html', {
        'ios_versions': versions.retrieve_ios_versions(with_unsupported=False),
        'android_versions': versions.retrieve_android_versions(with_unsupported=False)
    })


@login_required
def delete_version(request, _id):
    versions.delete_by_id(_id)
    return HttpResponseRedirect('/version/list')
