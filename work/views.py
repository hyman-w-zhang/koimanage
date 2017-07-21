import datetime

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from wcbp.common.dict_object import DictObject
from wcbp.model import Works, Templates

__works = Works()


@login_required
def list_work(request):
    __template = Templates()
    templates = __template.retrieve()
    return render(request, 'manage_works.html', {'templates': templates})


@login_required
def retrieve_works(request):
    page_no = int(request.POST.get('page_no', '') or 1)
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
