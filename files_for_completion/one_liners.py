def acronym(words):
    return "".join([x[0].upper() for x in words])


def median(numbers:list[int]):
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    middle = n //2
    return (sorted_numbers[middle] + sorted_numbers[-middle]) / 2


def make_alpha_dict(text):
    words = text.split()
    return {char: [word for word in words if char in word] for char in (''.join(words)) if char.isalpha()}


def flatten(lst):
    return [item for sublist in lst for item in (flatten(sublist) if isinstance(sublist, (list, tuple)) else [sublist])]

