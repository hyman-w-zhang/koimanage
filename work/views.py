import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from wcbp.common.dict_object import DictObject
from wcbp.model import Works
from wcbp.model import Templates
from wcbp.model import WorkCategories
from wcbp.model import Users


__works = Works()
__template = Templates()
__work_categories = WorkCategories()
__users = Users()


@login_required
def list_work(request):
    templates = __template.retrieve()
    return render(request, 'manage_works.html', {'templates': templates})


@login_required
def retrieve_works(request):
    page_no = int(request.POST.get('page', '') or 1)
    page_size = int(request.POST.get('page_size', '') or 10)
    created_start, created_end = None, None
    created_start_str = request.POST.get('created_date_begin', '')
    if created_start_str:
        created_start = datetime.datetime.strptime(created_start_str, 'yyyy-MM-dd')
    created_end_str = request.POST.get('created_date_end', '')
    if created_end_str:
        created_end = datetime.datetime.strptime(created_end_str, 'yyyy-MM-dd')
    template = request.POST.get('template', None)
    template = template if bool(template) else None

    works = __works.retrieve_all(template=template, page_no=page_no, page_size=page_size, created_start=created_start, created_end=created_end)
    for w in works:
        author = __users.from_id(w['author'])
        w['tel'] = author.get('tel', '')
        w['nickname'] = author.get('nikename', '')
        w['avatar'] = author.get('cover', '')
    data = {
        'total': __works.count(template=template, created_start=created_start, created_end=created_end),
        'works': works,
    }
    return JsonResponse(data, encoder=DictObject.JSONEncoder, safe=False)


@login_required
def audit_work(request):
    id = request.GET.get('id')
    __works.audit_work_by_id(id)
    return JsonResponse({'code': 0})


@login_required
def shelve_work(request):
    id = request.GET.get('id')
    __works.shelve_work_by_id(id)
    return JsonResponse({'code': 0})


@login_required
def add_work_category(request):
    return render(request, 'add_work_category.html')


@login_required
def save_work_category(request):
    name = request.POST.get('name')
    type = request.POST.get('type')
    __work_categories.save_category(name=name, type=type)
    return HttpResponseRedirect('/work/list_work_categories')


@login_required
def add_work_to_category(request):
    work_id = request.GET.get('work_id')
    category_id = request.GET.get('category_id')
    __work_categories.add_work_to_category(id=category_id, work_id=work_id)
    return JsonResponse({'code': 0})


@login_required
def sticky_work_to_category(request):
    work_id = request.GET.get('work_id')
    category_id = request.GET.get('category_id')
    __work_categories.sticky_work_to_category(id=category_id, work_id=work_id)
    return JsonResponse({'code': 0})


@login_required
def remove_work_from_category(request):
    work_id = request.GET.get('work_id')
    category_id = request.GET.get('category_id')
    __work_categories.remove_work_from_category(id=category_id, work_id=work_id)
    return JsonResponse({'code': 0})


@login_required
def save_category_works_order(request):
    id = request.POST.get('category_id')
    work_ids = request.POST.get('sorted_ids').split(',')
    __work_categories.save_works_order(id, work_ids)
    return HttpResponseRedirect('/work/list_work_categories')


@login_required
def list_work_categories(request):
    work_categories = __work_categories.retrieve()
    wc_list = list()
    for wc in work_categories:
        wc['id'] = str(wc['_id'])
        wc_list.append(wc)
    return render(request, 'list_work_categories.html', {'work_categories': wc_list})


@login_required
def manage_category_works(request):
    category_id = request.GET.get('id')
    work_category = __work_categories.from_id(id=category_id)
    works_id_list = work_category['works']
    works = __works.from_id_list(works_id_list, sort_as_input=True)
    for w in works:
        author = __users.from_id(w['author'])
        w['tel'] = author.get('tel', '')
        w['nickname'] = author.get('nikename', '')
        w['avatar'] = author.get('cover', '')
    return render(request, 'manage_category_works.html', {'works': works, 'category_id': category_id})


@login_required
def manage_work_categories(request):
    manual_work_categories = __work_categories.retrieve_manual()
    templates = __template.retrieve()
    wc_list = list()
    for wc in manual_work_categories:
        wc['id'] = str(wc['_id'])
        wc_list.append(wc)
    return render(request, 'manage_work_categories.html', {'categories': manual_work_categories, 'templates': templates})


@login_required
def retrieve_enable_works(request):
    page_no = int(request.POST.get('page', '') or 1)
    page_size = int(request.POST.get('page_size', '') or 10)
    created_start, created_end = None, None
    created_start_str = request.POST.get('created_date_begin', '')
    if created_start_str:
        created_start = datetime.datetime.strptime(created_start_str, 'yyyy-MM-dd')
    created_end_str = request.POST.get('created_date_end', '')
    if created_end_str:
        created_end = datetime.datetime.strptime(created_end_str, 'yyyy-MM-dd')
    template = request.POST.get('template', None)
    template = template if bool(template) else None

    category_id = request.POST.get('category_id', None)

    if bool(category_id):
        work_id_list = __work_categories.from_id(category_id)
        works = __works.from_id_list(id_list=work_id_list)
        total = len(work_id_list)

    else:
        works = __works.retrieve(template=template, page_no=page_no, page_size=page_size, created_start=created_start, created_end=created_end)
        total = __works.count_enable(template=template, created_start=created_start, created_end=created_end)

    manual_work_categories = __work_categories.retrieve_manual()
    work_list = list()
    for w in works:
        author = __users.from_id(w['author'])
        w['tel'] = author.get('tel', '')
        w['nickname'] = author.get('nikename', '')
        w['avatar'] = author.get('cover', '')
        w['categories_names'] = list()
        w['categories_ids'] = list()
        for wc in manual_work_categories:
            if bool(w['id']) and bool(wc['works']) and w['id'] in wc['works']:
                w['categories_names'].append(wc['name'])
                w['categories_ids'].append(wc['_id'])
        work_list.append(w)
    wc_list = list()
    for wc in manual_work_categories:
        wc['id'] = wc.pop('_id')
        wc_list.append(wc)

    data = {
        'total': total,
        'works': work_list,
        'categories': wc_list,
    }

    return JsonResponse(data, encoder=DictObject.JSONEncoder, safe=False)
