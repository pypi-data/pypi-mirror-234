"""Generates random piecewise polynomial functions (for example for testing CPD-algorithms)."""
from numbers import Integral
import random_partition_py as rpp
from typing import Callable, Optional
import numpy as np
from .pcw_fn import PcwPolynomial, PcwFn


__all__ = (
    "linear_transformation",
    "rnd_poly",
    "rnd_poly2",
    "rnd_pcw_poly",
    "PcwFn",
    "PcwPolynomial",
)


def linear_transformation(domain, image) -> Callable:
    """Returns the polynomial corresponding to the (affine) linear
    transformation mapping the domain (interval) onto the image (interval).
    """
    a = np.diff(image) / np.diff(domain)
    b = image[0] - domain[0] * a
    return np.polynomial.Polynomial(np.array((b[0], a[0])))


def rnd_poly(
        rng: np.random.Generator,
        dofs: int,
        domain: np.ndarray = np.array((0, 1)),
        codomain: np.ndarray = np.array((0, 1))
) -> np.polynomial.Polynomial:
    """Generate a random polynomial.

    The algorithm here is based on forcing the values of the polynomial on the boundary as well
    as at extremal values.
    """
    if dofs == 1:
        p = np.polynomial.Polynomial(
            rng.uniform(*codomain), domain=domain.copy())
    else:
        constraints_lhs = [
            np.hstack((1, np.zeros(dofs-1))),  # "entry" value
            np.ones(dofs),  # "exit" value
        ]
        constraints_rhs = [
            rng.uniform(*codomain),  # random from codom
            rng.uniform(*codomain),  # random from codom
        ]
        d = np.arange(dofs)
        for _ in range(dofs-2):
            x = rng.uniform(0, 1)  # random from domain
            y = rng.uniform(*codomain)  # random from codom
            constraints_lhs.append(x**d)  # value at x
            constraints_rhs.append(y)
            constraints_lhs.append(d * x**(d-1))  # derivative at x
            constraints_rhs.append(0.)
            # constraints_lhs.append(x**d - d * x**(d-1)) # forces value at point where derivative is zero
            # constraints_rhs.append(y) # to this value
        lhs = np.row_stack(constraints_lhs)
        coeffs = np.linalg.lstsq(lhs, constraints_rhs, rcond=None)[0]
        p = np.polynomial.Polynomial(coeffs)
        # rescale input to domain
        p = p(linear_transformation(domain, (0, 1)))
        # "crop" polynomial image to the prescribed image
        poly_vals = p(np.linspace(*domain, num=300))
        p_max = max(max(poly_vals), codomain[1])
        p_min = min(min(poly_vals), codomain[0])
        transform = linear_transformation(
            (p_min, p_max), (codomain[0], codomain[1]))
        p = transform(p)
    return p


def rnd_poly2(
        rng: np.random.Generator,
        dofs: int,
        domain: np.ndarray = np.array((0, 1)),
        image: np.ndarray = np.array((0, 1))
) -> np.polynomial.Polynomial:
    """Generate a random polynomial.

    The algorithm here is based on forcing random values to be on the graph and rescaling the result.
    """
    if dofs == 1:
        p = np.polynomial.Polynomial(rng.uniform(*image), domain=domain.copy())
    else:
        # generate random pairs of points to lie on the graph of the polynomial
        x = rng.uniform(domain[0], domain[1], size=dofs)
        y = rng.uniform(image[0], image[1], size=dofs)
        x = sorted(x)
        # fit a polynomial trough them
        p = np.polynomial.Polynomial.fit(
            x, y, deg=dofs - 1, domain=domain.copy())
        # sample the generated polynomial at some points to find its max and min
        poly_vals = p(np.linspace(*domain, num=300))
        p_max = max(max(poly_vals), image[1])
        p_min = min(min(poly_vals), image[0])
        # rescale polynomial output to match the image
        transform = linear_transformation((p_min, p_max), (image[0], image[1]))
        p = transform(p)
    return p


def rnd_pcw_poly(
    n_jumps: Integral,
    max_total_dofs: Integral,
    max_segment_dofs: Integral,
    jump_seed: Optional[Integral] = None,
    dof_seed: Optional[Integral] = None,
    realization_seed: Optional[Integral] = None,
) -> PcwPolynomial:
    """Generate a random piecewise polynomial function with domain and image [0,1].

    Args:
        n_jumps: Number of jumps ("discontinuities") in the result
        max_total_dofs: Maximum total number of degrees of freedom
            of the result where the number of degrees of freedom of
            a polynomial `p` is `1 + deg(p)`. Note that the generated
            pcw polynomial may have fewer dofs.
            Has to be larger than `n_jumps * max_segment_dof`.
        max_segment_dof`: Maximum local number of degrees of freedom.
        jump_seed: PRNG-seed for the jump locations.
        dof_seed: PRNG-seed for the local polynomial degrees.
        realization_seed: PRNG-seed for the specific realization of
            each local polynomial.

    Returns:
        A piecewise polynomial function matching the constraints.

    Example:
        Generate a random piecewise polynomial and plot it using matplotlib:
        ```
        import numpy as np
        import matplotlib.pyplot as plt

        p = rnd_pcw_poly(5, 200, 6)

        xs = np.linspace(0,1,5000)
        ys = p(xs)
        plt.scatter(xs, ys)
        plt.show()
        ```
    """
    # generate a random partition of the maximal degrees of freedom into the right number of parts
    dofs = rpp.random_partitions(
        max_total_dofs, n_jumps + 1, 1, seed=dof_seed)[0]
    # generate some random jump locations in (0, 1)
    jumps = np.sort(np.random.default_rng(
        seed=jump_seed).uniform(0+1e-12, 1-1e-12, n_jumps))
    borders = np.hstack([0., jumps, 1.])
    realization_rng = np.random.default_rng(seed=realization_seed)
    dof_rng = np.random.default_rng(seed=dof_seed)
    # generate a bunch of random polynomials using the dof partition and jump locations from above
    polys = [
        rnd_poly(
            realization_rng,
            dof_rng.integers(1, min(max_segment_dofs, d), endpoint=True),
            domain=borders[i:i+2],
        ) for (i, d) in enumerate(dofs)
    ]
    # setup a first pcw_poly
    pcw_poly = PcwPolynomial(polys, jumps)
    # normalize the polynomial
    # poly_vals = pcw_poly(np.linspace(*[0, 1], num=300))
    # p_max = max(poly_vals)
    # p_min = min(poly_vals)
    # # rescale polynomial output to [0,1]
    # transform = linear_transformation((p_min, p_max), (0, 1))
    # return PcwPolynomial([transform(p) for p in pcw_poly.funcs], jumps)
    return pcw_poly
