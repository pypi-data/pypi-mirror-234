import pandas as pd
from datetime import timedelta
from functools import partial, reduce
from typing import Any, Callable, Collection, List, Optional, Union

from .model import Leg, Trip

to_numeric = partial(pd.to_numeric, errors='coerce')


def _identity(x):
    return x


def get_data_frame(self: Union[Leg, Trip],
                   data_types: Union[str, Collection[str]],
                   resolution: Union[str, timedelta, None] = None,
                   conversion: Optional[Callable[[str], Any]] = to_numeric
                   ) -> pd.DataFrame:
    """
    Return available measurements as a time-series :code:`DataTable`.

    :code:`Series` will be named :code:`{TYPE}_{FIELD}` in the order given
    by :code:`data_types`.

    Data will be interpolated to the specified resolution.

    :param data_types: Data types to fetch.
    :param resolution: Target resolution. If :code:`None` (the default) then
        it will use the approximate resolution of the first requested type.
    :param conversion: Conversion to apply to all values. If :code:`None`
        then all values will be strings.
    """
    if isinstance(data_types, str):
        data_types = [data_types]

    if conversion is None:
        conversion = _identity

    collected: List[Any] = [([], []) for _ in data_types]
    data_type_idx = {data_type: idx
                     for idx, data_type in enumerate(data_types)}

    for m in self.get_data(include=data_types):
        idx = data_type_idx[m.type]
        collected[idx][0].append(pd.to_datetime(int(m.timestamp),
                                                unit='ms'))
        collected[idx][1].append(tuple(conversion(v)
                                       for v in m.data.split(',')))

    if resolution is None and len(data_types) > 1:
        try:
            resolution = collected[0][0][1] - collected[0][0][0]
        except IndexError:
            raise ValueError('No data for first type and no resolution given')

    new_index = None
    if resolution is not None:
        start = pd.to_datetime(self.start_time).ceil(resolution)
        end = pd.to_datetime(self.end_time).ceil(resolution)
        new_index = pd.date_range(start=start, end=end, freq=resolution)
        # np.datetime64 cannot hold timezone
        new_index = new_index.tz_localize(None)

    type_defs = self._client.get_types()

    for idx, data_type in enumerate(data_types):
        if len(collected[idx][0]) == 0:
            collected[idx] = pd.DataFrame()
            continue

        index = pd.DatetimeIndex(collected[idx][0])
        data = collected[idx][1]
        columns = ['{} {}'.format(data_type, field.name)
                   for field in type_defs[data_type].fields]
        collected[idx] = pd.DataFrame.from_records(data=data,
                                                   index=index,
                                                   columns=columns)
        if new_index is not None:
            if not index.is_unique:
                # https://csrf.atlassian.net/browse/PLAT-222
                collected[idx] = collected[idx][~index.duplicated()]
                index = collected[idx].index

            collected[idx].flags.allows_duplicate_labels = False
            collected[idx] = collected[idx] \
                .reindex(index.union(new_index)) \
                .interpolate(method='index') \
                .reindex(new_index)

    collected = [df for df in collected if not df.empty]
    if not collected:
        return pd.DataFrame()
    else:
        return reduce(pd.DataFrame.join, collected)


def get_gradient_frame(self: Leg, **kwargs) -> pd.DataFrame:
    """
    Return computed gradient data as a time-series :code:`DataTable`.

    :param leg: Parent leg object
    :param generate: Request and wait for generation if not available
    :param timeout: How long to wait if requesting generation
    """
    type_defs = self._client.get_types()
    columns = ['9 ' + field.name for field in type_defs['9'].fields]

    data = self.get_gradient(**kwargs)
    if not data:
        return pd.DataFrame()

    df = pd.DataFrame.from_records(
        ((pd.to_datetime(int(m.timestamp), unit='ms'), *(
            pd.to_numeric(v) for v in m.data.split(','))) for m in data),
        index='timestamp',
        columns=['timestamp', *columns]
    )
    return df


Leg.get_data_frame = get_data_frame
Trip.get_data_frame = get_data_frame
Leg.get_gradient_frame = get_gradient_frame
