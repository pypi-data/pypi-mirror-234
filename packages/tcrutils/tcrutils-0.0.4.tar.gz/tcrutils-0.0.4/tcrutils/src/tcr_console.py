import datetime
from functools import reduce

from colored import attr, bg, fg, stylize

from .tcr_extract_error import extract_error
from .tcr_print_iterable import print_iterable


class Console:
  def get_timestamp(self):
    return str(datetime.datetime.now())[:-3].replace(".", ",")

  def log     (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                        ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'I {self.get_timestamp()} ') + out
    out = stylize(out, fg("light_green") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def warn    (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                        ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'W {self.get_timestamp()} ') + out
    out = stylize(out, fg("yellow") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def error   (self, *values, sep=' ', end='', returnonly=False, withprefix=True                                        ) -> None or str:
    if not values: values = ['']
    values = [(extract_error(x) if isinstance(x, Exception) else x) for x in values]
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'E {self.get_timestamp()} ') + out
    out = stylize(out, fg("red") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
  def debug   (self, *values, sep=' ', end='', returnonly=False, withprefix=True, print_iterable_=True, passthrough=True) -> None or str:
    if not values: values = ['']
    if len(values) > 1:
      out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    else:
      out = values[0]
    if isinstance(out, type({}.values()) | type({}.keys())):
      out = list(out)
    if print_iterable_ and isinstance(out, list | tuple | dict):
      out = print_iterable(out, raw=True)
    out = str(out)
    if withprefix:
      out = (f'D {self.get_timestamp()} ') + out
    out = stylize(out, fg("magenta") + attr('bold'))# + attr("underlined"))
    if returnonly:
      return out
    print(out)
    return None if not passthrough else values[0]
  def critical(self, *values, sep=' ', end='', returnonly=False, withprefix=True                                        ) -> None or str:
    if not values: values = ['']
    out = reduce(lambda x, y: str(x) + sep + str(y), [*values, '']) + end
    if withprefix:
      out = (f'C {self.get_timestamp()} ') + out
    out = stylize(out, bg("red") + attr("bold"))
    if returnonly:
      return out
    print(out)
    return None
console = Console()
del Console