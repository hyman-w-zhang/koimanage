from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse

from utils import upload_material_file
from wcbp.model import Templates
from wcbp.model import TemplateCategories

from koimanage import versions

import time

__template_categories = TemplateCategories()
__templates = Templates()


@login_required
def add_template(request):
    id = str(ObjectId())
    return render(request, 'add_template.html', {'id': id, 'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})


@login_required
def save_template(request):
    id = request.POST['id']
    title = request.POST['title']
    # description = request.POST['description']
    # tags = request.POST['tags'].split(';')

    applicable = request.POST['applicable']
    scenario = request.POST['scenario']
    difficulty = float(request.POST['difficulty'])
    effect = request.POST['effect']

    material = request.FILES.get('material')
    material_file_name = upload_material_file.save_material_file(material, file_name=id)

    thumb = request.FILES.get('thumb')
    thumb_file_name = upload_material_file.save_thumb_file(thumb)

    poster = request.FILES.get('poster')
    poster_file_name = upload_material_file.save_poster_file(poster)

    video = request.FILES.get('video')
    video_file_name = upload_material_file.save_video_file(video)
    width, height, duration, file_size = upload_material_file.parse_video_info(video_file_name)

    origin_price = int(float(request.POST.get('origin_price')))
    on_sale_price = int(float(request.POST.get('on_sale_price')))

    ios_version = int(request.POST.get('ios_version'))
    android_version = int(request.POST.get('android_version'))
    version = int(time.time() * 1000)
    appstore_merchant_id = request.POST.get('appstore_merchant_id')

    template = Templates()
    template.save_template(id=id,
                           title=title,
                           tags=list(),
                           description='',
                           video=video_file_name,
                           thumb=thumb_file_name,
                           poster=poster_file_name,
                           width=width,
                           height=height,
                           duration=duration,
                           material=material_file_name,
                           origin_price=origin_price,
                           on_sale_price=on_sale_price,
                           ios_version=ios_version,
                           android_version=android_version,
                           version=version,
                           appstore_merchant_id=appstore_merchant_id,
                           applicable=applicable,
                           scenario=scenario,
                           difficulty=difficulty,
                           effect=effect
                           )

    template_category = TemplateCategories()
    template_category.add_template_to_default_category(id)

    return HttpResponseRedirect('/template/list')


@login_required
def modify_template(request):
    id = request.GET.get('id')
    template = Templates()
    t = template.from_id(id)
    t['tags'] = ';'.join(t['tags'])
    # t['on_sale_price'] /= 100
    # t['origin_price'] /= 100
    t.update(**{'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})
    return render(request, 'modify_template.html', t)


@login_required
def save_modify_template(request):
    id = request.POST['id']
    title = request.POST['title']
    # description = request.POST['description']
    # tags = request.POST['tags'].split(';')

    applicable = request.POST['applicable']
    scenario = request.POST['scenario']
    difficulty = float(request.POST['difficulty'])
    effect = request.POST['effect']

    material_file_name = None
    video_file_name = None
    thumb_file_name = None
    poster_file_name = None
    width, height, duration, file_size = None, None, None, None

    material = request.FILES.get('material')
    if bool(material):
        material_file_name = upload_material_file.save_material_file(material, file_name=id)

    thumb = request.FILES.get('thumb')
    if bool(thumb):
        thumb_file_name = upload_material_file.save_thumb_file(thumb)

    poster = request.FILES.get('poster')
    if bool(poster):
        poster_file_name = upload_material_file.save_poster_file(poster)

    video = request.FILES.get('video')
    if bool(video):
        video_file_name = upload_material_file.save_video_file(video)
        width, height, duration, file_size = upload_material_file.parse_video_info(video_file_name)

    origin_price = int(float(request.POST.get('origin_price')))
    on_sale_price = int(float(request.POST.get('on_sale_price')))
    ios_version = int(request.POST.get('ios_version'))
    android_version = int(request.POST.get('android_version'))
    available = 'valid'
    if ios_version == versions.UNSUPPORTED and android_version == versions.UNSUPPORTED:
        available = 'invalid'
    version = int(time.time() * 1000)
    appstore_merchant_id = request.POST.get('appstore_merchant_id')

    template = Templates()
    template.update_template(id=id,
                             title=title,
                             tags=None,
                             description=None,
                             video=video_file_name,
                             thumb=thumb_file_name,
                             poster=poster_file_name,
                             width=width,
                             height=height,
                             duration=duration,
                             material=material_file_name,
                             origin_price=origin_price,
                             on_sale_price=on_sale_price,
                             ios_version=ios_version,
                             android_version=android_version,
                             version=version,
                             appstore_merchant_id=appstore_merchant_id,
                             available=available,
                             applicable=applicable,
                             scenario=scenario,
                             difficulty=difficulty,
                             effect=effect
                             )

    return HttpResponseRedirect('/template/list')


@login_required
def list_template(request):
    template = Templates()
    templates = template.retrieve()

    template_categories = __template_categories.retrieve()
    template_list = list()
    for w in templates:
        w['categories_names'] = list()
        w['categories_ids'] = list()
        for wc in template_categories:
            if bool(w['id']) and bool(wc['templates']) and w['id'] in wc['templates']:
                w['categories_names'].append(wc['name'])
                w['categories_ids'].append(wc['_id'])
                template_list.append(w)
    tc_list = list()
    for tc in template_categories:
        tc['id'] = tc.pop('_id')
        tc_list.append(tc)

    return render(request, 'list_template.html', {'templates': templates, 'categories': tc_list})


@login_required
def add_template_category(request):
    template_categories = __template_categories.retrieve()
    order = 1
    for tc in template_categories:
        order += 1
    return render(request, 'add_template_category.html', {'order': order})


@login_required
def save_template_category(request):
    name = request.POST.get('name')
    order = request.POST.get('order')
    __template_categories.save_category(name=name, order=order)
    return HttpResponseRedirect('/template/list_template_categories')


@login_required
def add_template_to_category(request):
    template_id = request.GET.get('template_id')
    category_id = request.GET.get('category_id')
    __template_categories.add_template_to_category(id=category_id, template_id=template_id)
    return JsonResponse({'code': 0})


@login_required
def sticky_template_to_category(request):
    template_id = request.GET.get('template_id')
    category_id = request.GET.get('category_id')
    __template_categories.sticky_template_to_category(id=category_id, template_id=template_id)
    return JsonResponse({'code': 0})


@login_required
def remove_template_from_category(request):
    template_id = request.GET.get('template_id')
    category_id = request.GET.get('category_id')
    __template_categories.remove_template_from_category(id=category_id, template_id=template_id)
    return JsonResponse({'code': 0})


@login_required
def save_category_templates_order(request):
    id = request.POST.get('category_id')
    template_ids = request.POST.get('sorted_ids').split(',')
    __template_categories.save_templates_order(id, template_ids)
    return HttpResponseRedirect('/template/list_template_categories')


@login_required
def list_template_categories(request):
    template_categories = __template_categories.retrieve()
    wc_list = list()
    for wc in template_categories:
        wc['id'] = str(wc['_id'])
        wc_list.append(wc)
    return render(request, 'list_template_categories.html', {'template_categories': wc_list})


@login_required
def manage_category_templates(request):
    category_id = request.GET.get('id')
    template_category = __template_categories.from_id(id=category_id)
    templates_id_list = template_category['templates']
    templates = __templates.from_id_list(templates_id_list, sort_as_input=True)
    return render(request, 'manage_category_templates.html', {'templates': templates, 'category_id': category_id})
