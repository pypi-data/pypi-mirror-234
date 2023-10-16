from dataclasses import dataclass
from typing import Callable, Iterable, List
import numpy as np
import numpy.typing as npt
from numbers import Real
from bisect import bisect


@dataclass(frozen=True)
class PcwFn():
    """A piecewise function"""
    funcs: Iterable[Callable]
    jumps: Iterable[Real]  # must be sorted ascendingly

    def __call__(self, x: npt.ArrayLike) -> npt.ArrayLike:
        """Evaluate the function at some point (or an array of points)"""
        if isinstance(x, np.ndarray):
            xs = x.flatten()
            jumps = self.jumps
            funcs = self.funcs
            return np.array([funcs[bisect(jumps, x)](x) for x in xs]).reshape(x.shape)
        else:
            return self.funcs[bisect(self.jumps, x)](x)


@dataclass(frozen=True)
class PcwPolynomial(PcwFn):
    funcs: List[np.polynomial.Polynomial]
    jumps: npt.NDArray[np.float64]

    def __str__(self):
        body = (r") \\" "\n    ").join(f"{str(poly)} & x \\in [{poly.domain[0]}, {poly.domain[1]}"
                                       for poly in self.funcs
                                       )
        return r"\begin{cases}" f"\n{body}]\n" r"\end{cases}"

    def __format__(self, format_spec):
        body = (r") \\" "\n    ").join(f"{poly:{format_spec}} & x \\in [{poly.domain[0]}, {poly.domain[1]}"
                                       for poly in self.funcs
                                       )
        return r"\begin{cases}" f"\n{body}]\n" r"\end{cases}"
