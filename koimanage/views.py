from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from wcbp.model import ApiConfigs
from wcbp.model import Merchandises
from wcbp.model import Messages
from wcbp.model import Users
from . import versions

__api_config = ApiConfigs()

__merchandise = Merchandises()

__messages = Messages()

__users = Users()


@login_required
def admin_home(request):
    return render(request, 'base.html')


@login_required
def add_version(request):
    return render(request, 'add_version.html', {'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})


@login_required
def save_version(request):
    code = int(request.POST['code'])
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


@login_required
def add_api_config(request):
    id = str(ObjectId())
    return render(request, 'add_api_config.html', {
        'id': id,
        'ios_versions': versions.retrieve_ios_versions(with_unsupported=False),
        'android_versions': versions.retrieve_android_versions(with_unsupported=False)
    })


@login_required
def save_api_config(request):
    id = request.POST['id']
    min_ios_version = int(request.POST['min_ios_version'])
    min_android_version = int(request.POST['min_android_version'])
    latest_ios_version = int(request.POST['latest_ios_version'])
    latest_android_version = int(request.POST['latest_android_version'])
    apk_download_url = request.POST['apk_download_url']
    supported_pay = int(request.POST['supported_pay'])
    force_login = True if request.POST['force_login'] == '1' else False
    __api_config.save_api_config(id=id,
                                 min_ios_version=min_ios_version,
                                 min_android_version=min_android_version,
                                 latest_ios_version=latest_ios_version,
                                 latest_android_version=latest_android_version,
                                 apk_download_url=apk_download_url,
                                 supported_pay=supported_pay,
                                 force_login=force_login
                                 )
    return HttpResponseRedirect('/api_config/list')


@login_required
def retrieve_api_configs(request):
    ios_versions = versions.retrieve_ios_versions(with_unsupported=False)
    android_versions = versions.retrieve_android_versions(with_unsupported=False)
    return render(request, 'list_api_config.html', {
        'api_configs': __api_config.retrieve_api_configs(),
        'ios_versions': ios_versions,
        'android_versions': android_versions,
    })


@login_required
def delete_api_config(request, _id):
    __api_config.delete_api_config(_id)
    return HttpResponseRedirect('/api_config/list')


@login_required
def modify_api_config(request, _id):
    api_config = __api_config.get_config(_id)
    ios_versions = versions.retrieve_ios_versions(with_unsupported=False)
    android_versions = versions.retrieve_android_versions(with_unsupported=False)
    return render(request, 'modify_api_config.html', {
        'ios_versions': ios_versions,
        'android_versions': android_versions,
        **api_config
    })


@login_required
def save_modified_api_config(request):
    id = request.POST['id']
    min_ios_version = int(request.POST['min_ios_version'])
    min_android_version = int(request.POST['min_android_version'])
    latest_ios_version = int(request.POST['latest_ios_version'])
    latest_android_version = int(request.POST['latest_android_version'])
    apk_download_url = request.POST['apk_download_url']
    supported_pay = int(request.POST['supported_pay'])
    force_login = True if request.POST['force_login'] == '1' else False
    __api_config.update_api_config(id=id,
                                   min_ios_version=min_ios_version,
                                   min_android_version=min_android_version,
                                   latest_ios_version=latest_ios_version,
                                   latest_android_version=latest_android_version,
                                   apk_download_url=apk_download_url,
                                   supported_pay=supported_pay,
                                   force_login=force_login
                                   )
    return HttpResponseRedirect('/api_config/list')


@login_required
def add_merchandise(request):
    return render(request, 'add_merchandise.html')


@login_required
def save_merchandise(request):
    name = request.POST['name']
    type = request.POST['type']
    platform = request.POST['platform']
    appstore_merchandise_id = request.POST['appstore_merchandise_id']
    price = int(float(request.POST['price']) * 100)
    coin = int(request.POST['coin'])

    __merchandise.create(name=name, type=type, platform=platform, price=price, coin=coin, appstore_merchandise_id=appstore_merchandise_id)

    return HttpResponseRedirect('/merchandise/list')


@login_required
def list_merchandise(request):
    return render(request, 'list_merchandise.html')


@login_required
def retrieve_merchandises(request):
    type = None if not bool(request.POST['type']) else request.POST['type']
    status = None if not bool(request.POST['status']) else request.POST['status']
    platform = None if not bool(request.POST['platform']) else request.POST['platform']
    merchandises = __merchandise.retrieve(type=type, platform=platform, status=status)
    for merchandise in merchandises:
        merchandise['type'] = '锦鲤币' if merchandise['type'] == 'koicoin' else merchandise['type']
        merchandise['platform'] = '苹果' if merchandise['platform'] == 'iap' else '通用' if merchandise['platform'] == 'common' else merchandise['platform']
        merchandise['price'] /= 100.0
    return JsonResponse(merchandises, safe=False)


@login_required
def disable_merchandise(request, _id):
    __merchandise.disable_by_id(_id)
    return JsonResponse({'code': 0})


@login_required
def list_comments(request):
    return render(request, 'list_comments.html')


@login_required
def retrieve_comments(request):
    page = int(request.POST.get('page') or '1')
    page_size = int(request.POST.get('page_size') or '10')
    type = request.POST.get('type') or 'type'
    messages = __messages.list_message(type=type, res='0', page=page, page_size=page_size)
    for message in messages:
        message['nickname'] = __users.from_id(id=message['form'])['nikename']
    data = {'messages': messages, 'pages': [1, 2] + [i for i in range(max(3, page), 3 + max(3, page))], 'page': page}
    return JsonResponse(data, safe=False)


@login_required
def delete_comment(request):
    user_id = request.GET.get('user_id')
    msg_id = request.GET.get('msg_id')
    __messages.delete_message(uid=user_id, msg_id=msg_id)
    return JsonResponse({'code': 0})
