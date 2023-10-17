class Null:
  def __str__(self):
    return self.__repr__()
  def __repr__(self):
    return 'Null'
Null, _NullClass = Null(), Null

def _new(cls, *args, **kwargs):
  return Null
_NullClass.__new__ = _new
Null.__class__ = _NullClass

assert (Null) is (Null.__class__()) # No sneaky sneakies with making two different Nulls