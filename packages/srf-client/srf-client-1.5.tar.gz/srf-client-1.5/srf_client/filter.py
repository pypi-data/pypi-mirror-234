"""
Use with listing methods to filter the results.

    .. code:: python

        srf.trips.find_all(distance=between(0, 50))

Related entities can be traversed, which requires using dict syntax:

    .. code:: python

        srf.trips.find_all(**{'vehicle.make': eq('Scania')})

.. warning::
    Using unsupported operators for a field type will give unexpected
    results.
"""

from abc import ABC
from datetime import datetime, timedelta
from math import isinf

__all__ = [
    'Equals', 'Prefix', 'Between', 'Contains', 'AnyOf', 'Near',
    'eq', 'prefix', 'between', 'contains', 'any_of', 'near'
]

from geopy import Point
from geopy.distance import Distance


class Operator(ABC):
    def __init__(self, *values):
        self.values = [str(v) for v in values]

    def __iter__(self):
        return iter(self.values)


class Equals(Operator):
    """Field equals value."""

    def __init__(self, value):
        super().__init__(value)


class Prefix(Operator):
    """String field starts with value."""

    def __init__(self, value):
        super().__init__(str(value) + '*')


class Between(Operator):
    """Field is between two values (inclusive)."""

    def __init__(self, v1, v2):
        super().__init__(self._convert(v1), self._convert(v2))

    @staticmethod
    def _convert(value):
        if isinstance(value, datetime):
            return value.isoformat(timespec='milliseconds')
        elif isinstance(value, timedelta):
            return f'P{value.days}DT{value.seconds}.{value.microseconds:06}S'
        elif isinf(value):
            return 'Infinity' if value > 0 else '-Infinity'
        else:
            return value


class Contains(Operator):
    """Array field contains value(s)."""


class AnyOf(Operator):
    """String field matches any of these operators."""

    def __init__(self, *args: Operator):
        super().__init__(*(v for op in args for v in op.values))


class Near(Operator):
    """Point is within region centred on point."""

    def __init__(self, point: Point, distance: Distance):
        super().__init__(f'({point.latitude},{point.longitude}),{distance.km}')


eq = Equals
prefix = Prefix
between = Between
contains = Contains
any_of = AnyOf
near = Near
