from flask import current_app as app

def paginate(page_num, query):
    pages = query.paginate(page_num, app.config['ITEMS_PER_PAGE'], query)
    result = {
        'page': page_num,
        'result_count': pages.total,
        'has_next': pages.has_next,
        'has_prev': pages.has_prev,
    }

    result['results'] = [item.to_dict() for item in pages.items]
    return result
