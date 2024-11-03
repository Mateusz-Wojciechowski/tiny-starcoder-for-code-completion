def forall(pred, iterable):
    for item in iterable:
        if not pred(item):
            return False
    return True


def exists(pred, iterable):
    for item in iterable:
        if pred(item):
            return True
    return False


def atleast(pred, iterable, n):
    l = 0
    for item in iterable:
        if pred(item):
            l += 1
    return l >= n


def atmost(pred, iterable, n):
    l = 0
    for item in iterable:
        if pred(item):
            l += 1
    return l <= n
