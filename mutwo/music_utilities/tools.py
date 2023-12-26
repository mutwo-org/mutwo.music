import typing

__all__ = ("linear_space",)


def linear_space(start: float, end: float, sample_count: int = 50) -> typing.Generator:
    """Return evenly spaced numbers over a specified interval.

    :param start: The starting value of the sequence.
    :type start: float
    :param stop : The end value of the sequence.
    :param sample_count: int, Number of samples to generate.
        Default is 50. Must be non-negative.

    This is a simplified version of 'numpy.linspace'.
    """
    n = sample_count - 1
    Δ = end - start
    Δstep = Δ / n
    v = start
    for _ in range(n):
        yield v
        v += Δstep
    yield end
