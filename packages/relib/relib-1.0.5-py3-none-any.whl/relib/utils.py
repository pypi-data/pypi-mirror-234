from typing import TypeVar, Union, Iterable, Callable
from itertools import chain
import numpy as np
import re

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')

def list_split(l: list[T], sep: T) -> list[list[T]]:
  l = [sep, *l, sep]
  split_at = [i for i, x in enumerate(l) if x is sep]
  ranges = list(zip(split_at[0:-1], split_at[1:]))
  return [
    l[start + 1:end]
    for start, end in ranges
  ]

def drop_none(l: Iterable[Union[T, None]]) -> list[T]:
  return [x for x in l if x is not None]

def distinct(items: Iterable[T]) -> list[T]:
  return list(set(items))

def find(iterable: Iterable[T]) -> Union[T, None]:
  return next(iter(iterable), None)

def transpose_dict(des):
  if isinstance(des, list):
    keys = list(des[0].keys()) if des else []
    length = len(des)
    return {
      key: [des[i][key] for i in range(length)]
      for key in keys
    }
  elif isinstance(des, dict):
    keys = list(des.keys())
    length = len(des[keys[0]]) if keys else 0
    return [
      {key: des[key][i] for key in keys}
      for i in range(length)
    ]
  raise ValueError('transpose_dict only accepts dict or list')

def make_combinations_by_dict(des, keys=None, pairs=[]):
  keys = sorted(des.keys()) if keys == None else keys
  if len(keys) == 0:
    return [dict(pairs)]
  key = keys[0]
  remaining_keys = keys[1:]
  new_pairs = [(key, val) for val in des[key]]
  return flatten([
    make_combinations_by_dict(des, remaining_keys, [pair] + pairs)
    for pair in new_pairs
  ])

def merge_dicts(*dicts: dict[K, T]) -> dict[K, T]:
  output = {}
  for d in dicts:
    output.update(d)
  return output

def intersect(*lists: Iterable[T]) -> list[T]:
  return list(set.intersection(*map(set, lists)))

def ensure_tuple(value: Union[T, tuple[T, ...]]) -> tuple[T, ...]:
  return value if isinstance(value, tuple) else (value,)

def key_of(dicts: Iterable[dict[T, U]], key: T) -> list[U]:
  return [d[key] for d in dicts]

def omit(d: dict[K, T], keys: Iterable[K]) -> dict[K, T]:
  if keys:
    d = dict(d)
    for key in keys:
      del d[key]
  return d

def pick(d: dict[K, T], keys: Iterable[K]) -> dict[K, T]:
  return {key: d[key] for key in keys}

def dict_by(keys: Iterable[K], values: Iterable[T]) -> dict[K, T]:
  return dict(zip(keys, values))

def tuple_by(d: dict[K, T], keys: Iterable[K]) -> tuple[T, ...]:
  return tuple(d[key] for key in keys)

def flatten(l: Iterable[Iterable[T]]) -> list[T]:
  return list(chain.from_iterable(l))

def transpose(tuples, default_num_returns=0):
  output = tuple(zip(*tuples))
  if not output:
    return ([],) * default_num_returns
  return tuple(map(list, output))

def map_dict(fn: Callable[[T], U], d: dict[K, T]) -> dict[K, U]:
  return {key: fn(value) for key, value in d.items()}

def deepen_dict(d):
  output = {}
  for (*tail, head), value in d.items():
    curr = output
    for key in tail:
      if key not in curr:
        curr[key] = {}
      curr = curr[key]
    curr[head] = value
  return output

def group(pairs: Iterable[tuple[K, T]]) -> dict[K, list[T]]:
  values_by_key = {}
  for key, value in pairs:
    if key not in values_by_key:
      values_by_key[key] = []
    values_by_key[key].append(value)
  return values_by_key

def get_at(d, keys, default):
  try:
    for key in keys:
      d = d[key]
  except KeyError:
    return default
  return d

def sized_partitions(values: Iterable[T], part_size: int) -> list[list[T]]:
  if not isinstance(values, list):
    values = list(values)
  num_parts = (len(values) / part_size).__ceil__()
  return [values[i * part_size:(i + 1) * part_size] for i in range(num_parts)]

def num_partitions(values: Iterable[T], num_parts: int) -> list[list[T]]:
  if not isinstance(values, list):
    values = list(values)
  part_size = (len(values) / num_parts).__ceil__()
  return [values[i * part_size:(i + 1) * part_size] for i in range(num_parts)]

def _cat_tile(cats, n_tile):
    return cats[np.tile(np.arange(len(cats)), n_tile)]

def df_from_array(
  value_cols: dict[str, np.ndarray],
  dim_labels: list[tuple[str, list[Union[str, int, float]]]],
  indexed=False,
):
  import pandas as pd
  dim_names = [name for name, _ in dim_labels]
  dim_sizes = np.array([len(labels) for _, labels in dim_labels])
  assert all(array.shape == tuple(dim_sizes) for array in value_cols.values())
  repeats_tiles = [
    (dim_sizes[i + 1:].prod(), dim_sizes[:i].prod())
    for i in range(len(dim_sizes))
  ]
  label_arrays = [
    _cat_tile(pd.Categorical(labels).repeat(repeats), tiles)
    for labels, (repeats, tiles) in zip(dim_labels, repeats_tiles)
  ]
  category_cols = dict(zip(dim_names, label_arrays))
  value_cols = {name: array.reshape(-1) for name, array in value_cols.items()}
  df = pd.DataFrame({**category_cols, **value_cols}, copy=False)
  if indexed:
    df = df.set_index(dim_names)
  return df

StrFilter = Callable[[str], bool]

def str_filterer(
  include_patterns: list[re.Pattern[str]] = [],
  exclude_patterns: list[re.Pattern[str]] = [],
) -> StrFilter:
  def str_filter(string: str) -> bool:
    if any(pattern.search(string) for pattern in exclude_patterns):
      return False
    if not include_patterns:
      return True
    return any(pattern.search(string) for pattern in include_patterns)

  return str_filter
