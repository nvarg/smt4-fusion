from sqlalchemy import inspect

def dict_helper(obj):
    return iter({col.key: getattr(obj, col.key)
                 for col in inspect(obj).mapper.column_attrs}.items())
