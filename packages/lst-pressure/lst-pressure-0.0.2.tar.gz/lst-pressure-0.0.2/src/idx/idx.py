from intervaltree import IntervalTree

class IntervalIdx:
  def __init__(self):
    self.idx = IntervalTree()

  def insert(self,  begin, end, interval):
    self.idx[begin:end] = interval

  def envelop(self, begin, end):
    return self.idx.envelop(begin, end)

  # Get intervals that envelop some interval
  def reverse_lookup(self, interval):
    pass


