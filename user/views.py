from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from wcbp.common.dict_object import DictObject
from wcbp.model import Works
from wcbp.model import Templates
from wcbp.model import WorkCategories
from wcbp.model import Users
from utils import time_utils
from utils import page_utils
from wcbp.model import PayJournals
from wcbp.model import Merchandises
from wcbp.model import ConsumeJournals


__works = Works()
__template = Templates()
__work_categories = WorkCategories()
__users = Users()
__pay_journals = PayJournals()
__merchandises = Merchandises()
__consume_journals = ConsumeJournals()

templates_dict = {}
for t in __template.retrieve():
    templates_dict[t['id']] = t['title']


@login_required
def list_users(request):
    return render(request, 'list_users.html')


@login_required
def retrieve_users(request):
    page = int(request.POST.get('page', '') or 1)
    page_size = int(request.POST.get('page_size', '') or 10)
    created_start, created_end = None, None
    created_start_str = request.POST.get('created_start', '')
    if created_start_str:
        created_start = time_utils.datetime_str_to_milli_second_time_stamp(date_string=created_start_str)
    created_end_str = request.POST.get('created_end', '')
    if created_end_str:
        created_end = time_utils.datetime_str_to_milli_second_time_stamp(date_string=created_end_str)

    tel = request.POST.get('tel', None)
    nickname = request.POST.get('nickname', None)

    users = __users.retrieve_users(tel=tel, nickname=nickname, created_start=created_start, created_end=created_end, page_no=page, page_size=page_size)
    total = __users.count_users(tel=tel, nickname=nickname, created_start=created_start, created_end=created_end)
    max_page = (total + page_size - 1) // page_size
    for user in users:
        user['created_str'] = time_utils.milli_second_time_stamp_to_str(user['created'])

    data = {
        'total': total,
        'page_size': page_size,
        'max_page': max_page,
        'pages': page_utils.pages(start_page=1, cur_page=page, max_page=max_page),
        'page': page,
        'users': users,
    }
    return JsonResponse(data, encoder=DictObject.JSONEncoder, safe=False)


@login_required
def list_pay_journals(request):
    merchandises = __merchandises.retrieve()
    return render(request, 'list_pay_journals.html', {'merchandises': merchandises})


@login_required
def retrieve_pay_journals(request):
    page = int(request.POST.get('page', '') or 1)
    page_size = int(request.POST.get('page_size', '') or 10)
    created_start, created_end = None, None
    created_start_str = request.POST.get('created_start', '')
    if created_start_str:
        created_start = time_utils.datetime_str_to_milli_second_time_stamp(date_string=created_start_str)
    created_end_str = request.POST.get('created_end', '')
    if created_end_str:
        created_end = time_utils.datetime_str_to_milli_second_time_stamp(date_string=created_end_str)
    pay_type = request.POST.get('pay_type', None)
    merchandise_id = request.POST.get('merchandise_id', None)

    # user_id=None, merchandise_id=None, merchandise_type=None, page_size=20, page_no=1, pay_type=None, created_start=None, created_end=None
    pay_journals = __pay_journals.retrieve(merchandise_id=merchandise_id, page_size=page_size, page_no=page, pay_type=pay_type, created_start=created_start, created_end=created_end)
    total = __pay_journals.count(merchandise_id=merchandise_id, pay_type=pay_type, created_start=created_start, created_end=created_end)

    max_page = (total + page_size - 1) // page_size
    for pay_journal in pay_journals:
        user_id = pay_journal.get('user_id')
        if bool(user_id):
            user = __users.from_id(id=user_id)
            # pay_journal['user_cover'] = user['cover']
            pay_journal['user_tel'] = user.get('tel', '')
            pay_journal['user_nickname'] = user.get('nickname', '')
        pay_journal['pay_time_str'] = time_utils.milli_second_time_stamp_to_str(pay_journal['pay_time'])

    data = {
        'total': total,
        'page_size': page_size,
        'max_page': max_page,
        'pages': page_utils.pages(start_page=1, cur_page=page, max_page=max_page),
        'page': page,
        'pay_journals': pay_journals,
    }
    return JsonResponse(data, encoder=DictObject.JSONEncoder, safe=False)


@login_required
def list_consume_journals(request):
    merchandise_types = [
        {'id': 'template', 'name': '模板'},
    ]
    merchandises = [{'id': id, 'name': name} for id, name in templates_dict.items()]
    return render(request, 'list_consume_journals.html', {'merchandise_types': merchandise_types, 'merchandises': merchandises})


@login_required
def retrieve_consume_journals(request):
    page = int(request.POST.get('page', '') or 1)
    page_size = int(request.POST.get('page_size', '') or 10)
    created_start, created_end = None, None
    created_start_str = request.POST.get('created_start', '')
    if created_start_str:
        created_start = time_utils.parse_date_str_to_datetime(date_string=created_start_str)
    created_end_str = request.POST.get('created_end', '')
    if created_end_str:
        created_end = time_utils.parse_date_str_to_datetime(date_string=created_end_str)
    merchandise_type = request.POST.get('merchandise_type', None)
    merchandise_id = request.POST.get('merchandise_id', None)

    # user_id=None, merchandise_id=None, merchandise_type=None, page_size=20, page_no=1, created_start=None, created_end=None
    consume_journals = __consume_journals.retrieve(merchandise_type=merchandise_type, merchandise_id=merchandise_id, page_size=page_size, page_no=page, created_start=created_start, created_end=created_end)
    total = __consume_journals.count(merchandise_type=merchandise_type, merchandise_id=merchandise_id, created_start=created_start, created_end=created_end)

    max_page = (total + page_size - 1) // page_size
    for consume_journal in consume_journals:
        user_id = consume_journal.get('user_id')
        if bool(user_id):
            user = __users.from_id(id=user_id)
            # pay_journal['user_cover'] = user['cover']
            consume_journal['user_tel'] = user.get('tel', '')
            consume_journal['user_nickname'] = user.get('nickname', '')
            consume_journal['created_str'] = time_utils.format_datetime_to_datetime_str(consume_journal['created'])
        if consume_journal['merchandise_type'] == 'template':
            consume_journal['merchandise_name'] = __template.from_id(id=consume_journal['merchandise_id']).get('title')

    data = {
        'total': total,
        'page_size': page_size,
        'max_page': max_page,
        'pages': page_utils.pages(start_page=1, cur_page=page, max_page=max_page),
        'page': page,
        'consume_journals': consume_journals,
    }
    return JsonResponse(data, encoder=DictObject.JSONEncoder, safe=False)
