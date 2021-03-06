# Import other comps so they can be imported from this module
from ixmp.reporting.computations import *        # noqa: F401, F403
from ixmp.reporting.computations import product
from ixmp.reporting.utils import RENAME_DIMS, as_quantity

from .pyam import as_pyam, concat, write_report  # noqa: F401


def add(a, b, fill_value=0.0):
    """Sum of *a* and *b*."""
    return a.add(b, fill_value=fill_value).dropna()


def map_as_qty(set_df):
    """Convert *set_df* to a Quantity.

    For the MESSAGE sets named ``cat_*`` (see
    :ref:`mapping-sets`) :meth:`ixmp.Scenario.set` returns a
    :class:`~pandas.DataFrame` with two columns: the *category* set (S1)
    elements and the *category member* set (S2) elements.

    This computation converts the DataFrame *set_df* into a quantity with two
    dimensions. At the coordinates *(s₁, s₂)*, the value is 1 if *s₂* is a
    mapped from *s₁*; otherwise 0.

    See also
    --------
    broadcast_map
    """
    set_from, set_to = set_df.columns
    names = [RENAME_DIMS.get(c, c) for c in set_df.columns]

    # Add a value column
    set_df['value'] = 1

    return set_df.set_index([set_from, set_to])['value'] \
                 .rename_axis(index=names) \
                 .pipe(as_quantity)


def broadcast_map(quantity, map, rename={}):
    """Broadcast *quantity* using a *map*.

    The *map* must be a 2-dimensional quantity, such as returned by
    :meth:`map_as_qty`.

    *quantity* is 'broadcast' by multiplying it with the 2-dimensional *map*,
    and then dropping the common dimension. The result has the second dimension
    of *map* instead of the first.

    Parameters
    ----------
    rename : dict (str -> str), optional
        Dimensions to rename on the result.
    """
    return product(quantity, map).drop(map.dims[0]) \
                                 .rename(rename)
