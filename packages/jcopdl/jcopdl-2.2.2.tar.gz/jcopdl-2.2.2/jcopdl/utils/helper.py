def listify(item):
    if not isinstance(item, list):
        item = [item]
    return item
