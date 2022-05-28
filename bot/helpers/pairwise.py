from itertools import tee
from typing import Any, Iterable, Tuple


def pairwise(iterable: Iterable[Any]) -> Iterable[Tuple[Any, Any]]:
    """Create a 2-at-a-time iterable with overlapping.

    Typical example:

    >>>pairwise([1, 2, 3, 4, 5])
    [(1,2), (2,3), (3,4), (4,5)]
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
