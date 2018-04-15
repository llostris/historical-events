

def batch(iterable, batch_size=1):
    """Convenience function to make batching of various objects easier.
    :param iterable: iterable with a len function.
    :returns: a generator."""
    iterable_length = len(iterable)
    for index in range(0, iterable_length, batch_size):
        yield iterable[index:min(index + batch_size, iterable_length)]

