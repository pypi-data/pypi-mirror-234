def get_name_namespace_index(item):
    if isinstance(item, str) or isinstance(item, int):
        return item, None, 0
    size = len(item)
    if size > 1 and isinstance(item[0], str):
        if size == 2:
            if isinstance(item[1], (int, slice)):
                return item[0], None, item[1]
            if isinstance(item[1], str):
                return item[0], item[1], 0
            if item[1] is None:
                return item[0], None, 0
        if size == 3 and (item[1] is None or isinstance(item[1], str)) and \
                isinstance(item[2], (int, slice)):
            return item[0], item[1], item[2]
    raise ValueError


def get_name_namespace_value(item):
    size = len(item)
    if size > 0 and isinstance(item[0], str):
        # name, value
        if size == 2:
            return item[0], None, item[1]
        # name, namespace, value
        if size == 3 and (item[1] is None or isinstance(item[1], str)):
            return item[0], item[1], item[2]
    raise ValueError
