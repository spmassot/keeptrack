def left_join(left, left_key, right, right_key, right_attributes):
    keyed_rights = {getattr(r, right_key): r for r in right}
    prefix = next(iter(keyed_rights.values())).__class__.__name__
    for l in left:
        for attr in right_attributes:
            setattr(l, f'{prefix}_{attr}', getattr(keyed_rights[getattr(l, left_key)], attr))
    return left
