from utils import xlsx_utils


def test_save_to_xls():
    headers = [
        '用户名',
        '手机号',
    ]
    data_rows = [
        ['hyman', '18218814210', ],
        ['sin', '18610140491', ],
    ]
    full_file_name = xlsx_utils.save_to_xls(full_file_name=None, headers=headers, data_rows=data_rows)
    return full_file_name


def test_append_to_xls(full_file_name):
    data_rows = [
        ['colin', '13000000000', ],
    ] * 20
    xlsx_utils.save_to_xls(full_file_name=full_file_name, headers=None, data_rows=data_rows)


if __name__ == '__main__':
    import time

    time_start = time.time()
    _full_file_name = test_save_to_xls()
    print(_full_file_name)
    time_create = time.time()
    print('create_time: ', time_create - time_start)
    for i in range(100):
        test_append_to_xls(_full_file_name)
    time_append = time.time()
    print(time_append - time_create)
