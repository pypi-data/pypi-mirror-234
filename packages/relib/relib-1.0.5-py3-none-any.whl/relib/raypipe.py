import numpy as np

class Raypipe():
  def __init__(self, handlers=[]):
    self.handlers = handlers

  def __add_to_pipeline(self, handler_type, fn, kwargs={}):
    handler = (handler_type, fn, kwargs)
    return Raypipe(self.handlers + [handler])

  def map(self, fn):
    return self.__add_to_pipeline('map', fn)

  def flatten(self):
    return self.__add_to_pipeline('flatten', None)

  def flat_map(self, fn):
    return self.map(fn).flatten()

  def filter(self, fn):
    return self.__add_to_pipeline('filter', fn)

  def sort(self, fn=None, reverse=False):
    return self.__add_to_pipeline('sort', fn, dict(reverse=reverse))

  def distinct(self):
    return self.__add_to_pipeline('distinct', None)

  def sort_distinct(self, fn=None, reverse=False):
    return self.distinct().sort(fn, reverse=reverse)

  def do(self, fn):
    return self.__add_to_pipeline('do', fn)

  def shuffle(self, random_state=42):
    return self.__add_to_pipeline('shuffle', None, dict(random_state=random_state))

  def to_numpy(self):
    return self.__add_to_pipeline('do', np.array)

  def compute(self, values):
    for handler_type, handler_fn, handler_kwargs in self.handlers:
      if handler_type == 'map':
        values = [handler_fn(val) for val in values]
      elif handler_type == 'flatten':
        values = [item for sublist in values for item in sublist]
      elif handler_type == 'filter':
        values = [val for val in values if handler_fn(val)]
      elif handler_type == 'sort':
        values.sort(key=handler_fn, reverse=handler_kwargs['reverse'])
      elif handler_type == 'distinct':
        values = list(set(values))
      elif handler_type == 'do':
        values = handler_fn(values)
      elif handler_type == 'shuffle':
        from sklearn.utils import shuffle
        values = shuffle(values, random_state=handler_kwargs['random_state'])
    return values

raypipe = Raypipe()
