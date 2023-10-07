from time import time
from termcolor import colored

active_mds = []

class measure_duration:
  def __init__(self, name):
    self.name = name
    self.start = time()
    active_mds.append(self)

  def __enter__(self):
    pass

  def __exit__(self, *_):
    duration = round(time() - self.start, 4)
    indent_level = len(active_mds) - 1
    indentatation = ('──' * indent_level) + (' ' * (indent_level > 0))
    text = '{}: {} seconds'.format(self.name, duration)
    print(colored(indentatation + text, attrs=['dark']))
    active_mds.remove(self)
