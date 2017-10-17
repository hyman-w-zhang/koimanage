from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from wcbp.model import ApiConfigs
from wcbp.model import Merchandises
from wcbp.model import Messages
from wcbp.model import Users
from wcbp.model import Banners
from wcbp.model import TemplateCategories
from wcbp.model import WorkCategories
from wcbp.model import IndexAds
from wcbp.model import Activities
from . import versions
from utils import time_utils
from utils import upload_material_file

__api_config = ApiConfigs()

__merchandise = Merchandises()

__messages = Messages()

__users = Users()

__banners = Banners()

__template_categories = TemplateCategories()
__work_categories = WorkCategories()
__index_ads = IndexAds()
__activities = Activities()


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
    res = request.POST.get('res') or '0'
    messages = __messages.list_message(type=type, res=res, page=page, page_size=page_size)
    for message in messages:
        message['nickname'] = __users.from_id(id=message['form'])['nikename']
        message['created_str'] = time_utils.milli_second_time_stamp_to_str(message['created'])
    data = {'messages': messages, 'pages': [1, 2] + [i for i in range(max(3, page), 3 + max(3, page))], 'page': page}
    return JsonResponse(data, safe=False)


@login_required
def delete_comment(request):
    user_id = request.GET.get('user_id')
    msg_id = request.GET.get('msg_id')
    __messages.delete_message(uid=user_id, msg_id=msg_id)
    return JsonResponse({'code': 0})


@login_required
def add_banner(request):
    count = __banners.count() or 0
    return render(request, 'add_banner.html', {'order': count + 1, 'id': str(ObjectId())})


@login_required
def save_banner(request):
    order = int(request.POST['order'])
    link = request.POST['link']
    id = request.POST['id']
    cover_file = request.FILES.get('cover_file')
    cover_file_name = None
    if bool(cover_file):
        cover_file_name = upload_material_file.save_poster_file(cover_file)
    __banners.save_banner(id=id, link=link, cover=cover_file_name, order=order)
    return HttpResponseRedirect('/banner/list')


@login_required
def list_banner(request):
    banners = __banners.retrieve()
    return render(request, 'list_banner.html', {'banners': banners})


@login_required
def disable_banner(request):
    id = request.GET['id']
    __banners.update_banner(id, status='disabled')
    return JsonResponse({'code': 0})


@login_required
def save_banners_order(request):
    banner_ids = request.POST['ids'].split(',')
    __banners.save_banners_sort(*banner_ids)
    return JsonResponse({'code': 0, 'msg': '保存排序成功'})


@login_required
def retrieve_index_ads(request):
    return render(request, 'list_index_ad.html', {
        'index_ads': __index_ads.retrieve()
    })


@login_required
def modify_index_ad(request, _id):
    index_ad = __index_ads.from_id(_id)
    link_types = [
        {'code': 0, 'name': '外链'},
        {'code': 1, 'name': '首页其他TAB'},
        {'code': 2, 'name': '模板页指定TAB'},
    ]
    link_pages = [
        {'code': -1, 'name': '外链'},
        {'code': 0, 'name': '首页'},
        {'code': 1, 'name': '模板'},
    ]
    wc_list = __work_categories.retrieve()
    work_categories = list()
    for wc in wc_list:
        work_categories.append({'id': str(wc['_id']), 'name': wc['name']})

    tc_list = __template_categories.retrieve()
    template_categories = list()
    for tc in tc_list:
        template_categories.append({'id': str(tc['_id']), 'name': tc['name']})

    return render(request, 'modify_index_ad.html', {
        **index_ad,
        'link_types': link_types,
        'link_pages': link_pages,
        'work_categories': work_categories,
        'template_categories': template_categories,
    })


@login_required
def save_modified_index_ad(request):
    id = request.POST['id']
    cover_file = request.FILES.get('cover_file')
    cover_file_name = None
    if bool(cover_file):
        cover_file_name = upload_material_file.save_poster_file(cover_file)
    link_type = int(request.POST['link_type'])
    link_tab = ''
    link_page = int(request.POST.get('link_page'))
    link = ''
    if link_type == 0:
        link = request.POST['link']
    elif link_type == 1:
        link_tab = request.POST.get('work_category')
        link = 'javascript:locate_to_category("{link_tab}");'.format(link_tab=link_tab)
    elif link_type == 2:
        link_tab = request.POST.get('template_category')
        link = 'javascript:locate_to_tab_and_category("{link_page}","{link_tab}");'.format(link_page=link_page, link_tab=link_tab)

    __index_ads.update_index_ad(id, cover=cover_file_name, link=link, link_page=link_page, link_tab=link_tab, link_type=link_type)
    return HttpResponseRedirect('/index_ad/list')


@login_required
def retrieve_activities(request):
    return render(request, 'list_activity.html', {
        'activities': __activities.retrieve()
    })


@login_required
def modify_activity(request, _id):
    activity = __activities.from_id(_id)
    link_types = [
        {'code': 0, 'name': '外链'},
        {'code': 1, 'name': '首页其他TAB'},
        {'code': 2, 'name': '模板页指定TAB'},
    ]
    link_pages = [
        {'code': -1, 'name': '外链'},
        {'code': 0, 'name': '首页'},
        {'code': 1, 'name': '模板'},
    ]
    wc_list = __work_categories.retrieve()
    work_categories = list()
    for wc in wc_list:
        work_categories.append({'id': str(wc['_id']), 'name': wc['name']})

    tc_list = __template_categories.retrieve()
    template_categories = list()
    for tc in tc_list:
        template_categories.append({'id': str(tc['_id']), 'name': tc['name']})

    return render(request, 'modify_activity.html', {
        **activity,
        'link_types': link_types,
        'link_pages': link_pages,
        'work_categories': work_categories,
        'template_categories': template_categories,
    })


@login_required
def save_modified_activity(request):
    id = request.POST['id']
    cover_file = request.FILES.get('cover_file')
    cover_file_name = None
    if bool(cover_file):
        cover_file_name = upload_material_file.save_poster_file(cover_file)
    link_type = int(request.POST['link_type'])
    link_tab = ''
    link_page = int(request.POST.get('link_page'))
    link = ''
    if link_type == 0:
        link = request.POST['link']
    elif link_type == 1:
        link_tab = request.POST.get('work_category')
        link = 'javascript:locate_to_category("{link_tab}");'.format(link_tab=link_tab)
    elif link_type == 2:
        link_tab = request.POST.get('template_category')
        link = 'javascript:locate_to_tab_and_category("{link_page}","{link_tab}");'.format(link_page=link_page, link_tab=link_tab)

    __activities.update_activity(id, cover=cover_file_name, link=link, link_page=link_page, link_tab=link_tab, link_type=link_type)
    return HttpResponseRedirect('/activity/list')
