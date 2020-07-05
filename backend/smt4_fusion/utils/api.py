import functools

from flask import current_app as app
from webargs.multidictproxy import MultiDictProxy
from webargs.flaskparser import parser

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


@parser.location_loader("query_and_json")
def load_data(request, schema):
    data = request.args.copy()
    data.update(request.get_json() or {})
    return MultiDictProxy(data, schema)

def freeze_args(func):

    class _FrozenArgs(dict):
        def __hash__(self):
            return hash(frozenset(self.items()))

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([_FrozenArgs(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: _FrozenArgs(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)

    return wrapped
