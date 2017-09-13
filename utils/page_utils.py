def pages(start_page=1, cur_page=1, max_page=1):
    if not start_page <= cur_page <= max_page:
        return []
    if max_page <= 5:
        return [str(i) for i in range(start_page, max_page + 1)]
    elif cur_page <= 2:
        return ['1', '2', '3', '...', str(max_page - 1), str(max_page), ]
    elif cur_page >= max_page - 1:
        return ['1', '2', '...', str(max_page - 2), str(max_page - 1), str(max_page), ]
    else:
        return ['1', '...', str(cur_page - 1), str(cur_page), str(cur_page + 1), '...', str(max_page), ]