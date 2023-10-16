from typing import Sequence as Sequence5, Any as Any8
from builtins import int as int10, bool as bool0, str as str2
from temper_core import int_to_string as int_to_string_1224, string_code_points as string_code_points_1225, str_cat as str_cat_1223
# Type nym`std//temporal.temper.md`.Date connected to datetime.date
daysInMonth__21: 'Sequence5[int10]' = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
def isLeapYear__19(year__22: 'int10') -> 'bool0':
  return__13: 'bool0'
  t_132: 'int10'
  if year__22 % 4 == 0:
    if year__22 % 100 != 0:
      return__13 = True
    else:
      t_132 = year__22 % 400
      return__13 = t_132 == 0
  else:
    return__13 = False
  return return__13
def pad__20(padding__24: 'str2', num__25: 'int10') -> 'str2':
  global int_to_string_1224, string_code_points_1225
  return__14: 'str2'
  t_185: 'Any8'
  decimal__27: 'str2' = int_to_string_1224(num__25, 10)
  t_181: 'Any8' = string_code_points_1225(decimal__27)
  decimalCodePoints__28: 'Any8' = t_181
  sign__29: 'str2'
  if decimalCodePoints__28.read() == 45:
    sign__29 = '-'
    t_185 = decimalCodePoints__28.advance(1)
    decimalCodePoints__28 = t_185
  else:
    sign__29 = ''
  paddingCp__30: 'Any8' = string_code_points_1225(padding__24)
  nNeeded__31: 'int10' = paddingCp__30.length - decimalCodePoints__28.length
  if nNeeded__31 <= 0:
    return__14 = decimal__27
  else:
    pad__32: 'str2' = paddingCp__30.limit(nNeeded__31).to_string()
    decimalOnly__33: 'str2' = decimalCodePoints__28.to_string()
    return__14 = str_cat_1223(sign__29, pad__32, decimalOnly__33)
  return return__14
