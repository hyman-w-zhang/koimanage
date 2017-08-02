from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from utils import upload_material_file
from wcbp.model.template import Templates

from koimanage import versions

import time


@login_required
def add_template(request):
    id = str(ObjectId())
    return render(request, 'add_template.html', {'id': id, 'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})


@login_required
def save_template(request):
    id = request.POST['id']
    title = request.POST['title']
    description = request.POST['description']
    tags = request.POST['tags'].split(';')

    material = request.FILES.get('material')
    material_file_name = upload_material_file.save_material_file(material, file_name=id)

    thumb = request.FILES.get('thumb')
    thumb_file_name = upload_material_file.save_thumb_file(thumb)

    poster = request.FILES.get('poster')
    poster_file_name = upload_material_file.save_poster_file(poster)

    video = request.FILES.get('video')
    video_file_name = upload_material_file.save_video_file(video)
    width, height, duration, file_size = upload_material_file.parse_video_info(video_file_name)

    origin_price = int(100 * float(request.POST.get('origin_price')))
    on_sale_price = int(100 * float(request.POST.get('on_sale_price')))

    ios_version = int(request.POST.get('ios_version'))
    android_version = int(request.POST.get('android_version'))
    version = int(time.time() * 1000)
    appstore_merchant_id = request.POST.get('appstore_merchant_id')

    template = Templates()
    template.save_template(id=id,
                           title=title,
                           tags=tags,
                           description=description,
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
                           appstore_merchant_id=appstore_merchant_id
                           )

    return HttpResponseRedirect('/template/list')


@login_required
def modify_template(request):
    id = request.GET.get('id')
    template = Templates()
    t = template.from_id(id)
    t['tags'] = ';'.join(t['tags'])
    t['on_sale_price'] /= 100
    t['origin_price'] /= 100
    t.update(**{'ios_versions': versions.retrieve_ios_versions(), 'android_versions': versions.retrieve_android_versions()})
    return render(request, 'modify_template.html', t)


@login_required
def save_modify_template(request):
    id = request.POST['id']
    title = request.POST['title']
    description = request.POST['description']
    tags = request.POST['tags'].split(';')

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

    origin_price = int(100 * float(request.POST.get('origin_price')))
    on_sale_price = int(100 * float(request.POST.get('on_sale_price')))
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
                             tags=tags,
                             description=description,
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
                             available=available
                             )

    return HttpResponseRedirect('/template/list')


@login_required
def list_template(request):
    template = Templates()
    templates = template.retrieve()
    for t in templates:
        t['on_sale_price'] /= 100
        t['origin_price'] /= 100
    return render(request, 'list_template.html', {'templates': templates})
