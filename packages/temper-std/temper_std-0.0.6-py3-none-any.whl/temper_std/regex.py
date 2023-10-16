from abc import ABCMeta as ABCMeta13
from builtins import str as str2, bool as bool0, int as int10, Exception as Exception9, len as len_1220, list as list_1215
from types import MappingProxyType as MappingProxyType14
from typing import Callable as Callable3, Sequence as Sequence5, Optional as Optional7, Union as Union6, Any as Any8, MutableSequence as MutableSequence1
from temper_core import cast_by_type as cast_by_type15, Label as Label11, BubbleException as BubbleException12, isinstance_int as isinstance_int16, cast_by_test as cast_by_test17, list_join as list_join_1214, generic_eq as generic_eq_1232, list_builder_add as list_builder_add_1210, string_code_points as string_code_points_1225, list_get as list_get_1221, str_cat as str_cat_1223, int_to_string as int_to_string_1224
from temper_core.regex import compiled_regex_compile_formatted as compiled_regex_compile_formatted_1226, compiled_regex_compiled_found as compiled_regex_compiled_found_1227, compiled_regex_compiled_find as compiled_regex_compiled_find_1228, compiled_regex_compiled_replace as compiled_regex_compiled_replace_1229, regex_formatter_push_capture_name as regex_formatter_push_capture_name_1233, regex_formatter_push_code_to as regex_formatter_push_code_to_1234
class Regex(metaclass = ABCMeta13):
  def compiled(this__8) -> 'CompiledRegex':
    return CompiledRegex(this__8)
  def found(this__9, text__121: 'str2') -> 'bool0':
    return this__9.compiled().found(text__121)
  def find(this__10, text__124: 'str2') -> 'MappingProxyType14[str2, Group]':
    return this__10.compiled().find(text__124)
  def replace(this__11, text__127: 'str2', format__128: 'Callable3[[MappingProxyType14[str2, Group]], str2]') -> 'str2':
    return this__11.compiled().replace(text__127, format__128)
class Capture(Regex):
  name__130: 'str2'
  item__131: 'Regex'
  __slots__ = ('name__130', 'item__131')
  def constructor__132(this__50, name__133: 'str2', item__134: 'Regex') -> 'None':
    this__50.name__130 = name__133
    this__50.item__131 = item__134
  def __init__(this__50, name__133: 'str2', item__134: 'Regex') -> None:
    this__50.constructor__132(name__133, item__134)
  @property
  def name(this__298) -> 'str2':
    return this__298.name__130
  @property
  def item(this__302) -> 'Regex':
    return this__302.item__131
class CodePart(Regex, metaclass = ABCMeta13):
  pass
class CodePoints(CodePart):
  value__135: 'str2'
  __slots__ = ('value__135',)
  def constructor__136(this__52, value__137: 'str2') -> 'None':
    this__52.value__135 = value__137
  def __init__(this__52, value__137: 'str2') -> None:
    this__52.constructor__136(value__137)
  @property
  def value(this__306) -> 'str2':
    return this__306.value__135
class Special(Regex, metaclass = ABCMeta13):
  pass
class SpecialSet(CodePart, Special, metaclass = ABCMeta13):
  pass
class CodeRange(CodePart):
  min__145: 'int10'
  max__146: 'int10'
  __slots__ = ('min__145', 'max__146')
  def constructor__147(this__68, min__148: 'int10', max__149: 'int10') -> 'None':
    this__68.min__145 = min__148
    this__68.max__146 = max__149
  def __init__(this__68, min__148: 'int10', max__149: 'int10') -> None:
    this__68.constructor__147(min__148, max__149)
  @property
  def min(this__310) -> 'int10':
    return this__310.min__145
  @property
  def max(this__314) -> 'int10':
    return this__314.max__146
class CodeSet(Regex):
  items__150: 'Sequence5[CodePart]'
  negated__151: 'bool0'
  __slots__ = ('items__150', 'negated__151')
  def constructor__152(this__70, items__153: 'Sequence5[CodePart]', negated: Optional7['bool0'] = None) -> 'None':
    negated__154: Optional7['bool0'] = negated
    if negated__154 is None:
      negated__154 = False
    this__70.items__150 = items__153
    this__70.negated__151 = negated__154
  def __init__(this__70, items__153: 'Sequence5[CodePart]', negated: Optional7['bool0'] = None) -> None:
    negated__154: Optional7['bool0'] = negated
    this__70.constructor__152(items__153, negated__154)
  @property
  def items(this__318) -> 'Sequence5[CodePart]':
    return this__318.items__150
  @property
  def negated(this__322) -> 'bool0':
    return this__322.negated__151
class Or(Regex):
  items__155: 'Sequence5[Regex]'
  __slots__ = ('items__155',)
  def constructor__156(this__73, items__157: 'Sequence5[Regex]') -> 'None':
    this__73.items__155 = items__157
  def __init__(this__73, items__157: 'Sequence5[Regex]') -> None:
    this__73.constructor__156(items__157)
  @property
  def items(this__326) -> 'Sequence5[Regex]':
    return this__326.items__155
class Repeat(Regex):
  item__158: 'Regex'
  min__159: 'int10'
  max__160: 'Union6[int10, None]'
  reluctant__161: 'bool0'
  __slots__ = ('item__158', 'min__159', 'max__160', 'reluctant__161')
  def constructor__162(this__76, item__163: 'Regex', min__164: 'int10', max__165: 'Union6[int10, None]', reluctant: Optional7['bool0'] = None) -> 'None':
    reluctant__166: Optional7['bool0'] = reluctant
    if reluctant__166 is None:
      reluctant__166 = False
    this__76.item__158 = item__163
    this__76.min__159 = min__164
    this__76.max__160 = max__165
    this__76.reluctant__161 = reluctant__166
  def __init__(this__76, item__163: 'Regex', min__164: 'int10', max__165: 'Union6[int10, None]', reluctant: Optional7['bool0'] = None) -> None:
    reluctant__166: Optional7['bool0'] = reluctant
    this__76.constructor__162(item__163, min__164, max__165, reluctant__166)
  @property
  def item(this__330) -> 'Regex':
    return this__330.item__158
  @property
  def min(this__334) -> 'int10':
    return this__334.min__159
  @property
  def max(this__338) -> 'Union6[int10, None]':
    return this__338.max__160
  @property
  def reluctant(this__342) -> 'bool0':
    return this__342.reluctant__161
class Sequence(Regex):
  items__175: 'Sequence5[Regex]'
  __slots__ = ('items__175',)
  def constructor__176(this__82, items__177: 'Sequence5[Regex]') -> 'None':
    this__82.items__175 = items__177
  def __init__(this__82, items__177: 'Sequence5[Regex]') -> None:
    this__82.constructor__176(items__177)
  @property
  def items(this__346) -> 'Sequence5[Regex]':
    return this__346.items__175
class Group:
  name__178: 'str2'
  value__179: 'str2'
  codePointsBegin__180: 'int10'
  __slots__ = ('name__178', 'value__179', 'codePointsBegin__180')
  def constructor__181(this__85, name__182: 'str2', value__183: 'str2', codePointsBegin__184: 'int10') -> 'None':
    this__85.name__178 = name__182
    this__85.value__179 = value__183
    this__85.codePointsBegin__180 = codePointsBegin__184
  def __init__(this__85, name__182: 'str2', value__183: 'str2', codePointsBegin__184: 'int10') -> None:
    this__85.constructor__181(name__182, value__183, codePointsBegin__184)
  @property
  def name(this__350) -> 'str2':
    return this__350.name__178
  @property
  def value(this__354) -> 'str2':
    return this__354.value__179
  @property
  def code_points_begin(this__358) -> 'int10':
    return this__358.codePointsBegin__180
class RegexRefs__19:
  codePoints__185: 'CodePoints'
  group__186: 'Group'
  orObject__187: 'Or'
  __slots__ = ('codePoints__185', 'group__186', 'orObject__187')
  def constructor__188(this__87, code_points: Optional7['CodePoints'] = None, group: Optional7['Group'] = None, or_object: Optional7['Or'] = None) -> 'None':
    codePoints__189: Optional7['CodePoints'] = code_points
    group__190: Optional7['Group'] = group
    orObject__191: Optional7['Or'] = or_object
    t_1143: 'CodePoints'
    t_1145: 'Group'
    t_1147: 'Or'
    if codePoints__189 is None:
      t_1143 = CodePoints('')
      codePoints__189 = t_1143
    if group__190 is None:
      t_1145 = Group('', '', 0)
      group__190 = t_1145
    if orObject__191 is None:
      t_1147 = Or(())
      orObject__191 = t_1147
    this__87.codePoints__185 = codePoints__189
    this__87.group__186 = group__190
    this__87.orObject__187 = orObject__191
  def __init__(this__87, code_points: Optional7['CodePoints'] = None, group: Optional7['Group'] = None, or_object: Optional7['Or'] = None) -> None:
    codePoints__189: Optional7['CodePoints'] = code_points
    group__190: Optional7['Group'] = group
    orObject__191: Optional7['Or'] = or_object
    this__87.constructor__188(codePoints__189, group__190, orObject__191)
  @property
  def code_points(this__362) -> 'CodePoints':
    return this__362.codePoints__185
  @property
  def group(this__366) -> 'Group':
    return this__366.group__186
  @property
  def or_object(this__370) -> 'Or':
    return this__370.orObject__187
class CompiledRegex:
  data__192: 'Regex'
  compiled__206: 'Any8'
  __slots__ = ('data__192', 'compiled__206')
  def constructor__193(this__20, data__194: 'Regex') -> 'None':
    this__20.data__192 = data__194
    t_1137: 'str2' = this__20.format__225()
    t_1138: 'Any8' = compiled_regex_compile_formatted_1226(this__20, t_1137)
    this__20.compiled__206 = t_1138
  def __init__(this__20, data__194: 'Regex') -> None:
    this__20.constructor__193(data__194)
  def found(this__21, text__197: 'str2') -> 'bool0':
    return compiled_regex_compiled_found_1227(this__21, this__21.compiled__206, text__197)
  def find(this__22, text__200: 'str2') -> 'MappingProxyType14[str2, Group]':
    return compiled_regex_compiled_find_1228(this__22, this__22.compiled__206, text__200, regexRefs__117)
  def replace(this__23, text__203: 'str2', format__204: 'Callable3[[MappingProxyType14[str2, Group]], str2]') -> 'str2':
    return compiled_regex_compiled_replace_1229(this__23, this__23.compiled__206, text__203, format__204, regexRefs__117)
  def format__225(this__28) -> 'str2':
    return RegexFormatter__29().format(this__28.data__192)
  @property
  def data(this__374) -> 'Regex':
    return this__374.data__192
class RegexFormatter__29:
  out__227: 'MutableSequence1[str2]'
  __slots__ = ('out__227',)
  def format(this__30, regex__229: 'Regex') -> 'str2':
    this__30.pushRegex__232(regex__229)
    t_1120: 'MutableSequence1[str2]' = this__30.out__227
    def fn__1117(x__231: 'str2') -> 'str2':
      return x__231
    return list_join_1214(t_1120, '', fn__1117)
  def pushRegex__232(this__31, regex__233: 'Regex') -> 'None':
    t_737: 'bool0'
    t_738: 'Capture'
    t_741: 'bool0'
    t_742: 'CodePoints'
    t_745: 'bool0'
    t_746: 'CodeRange'
    t_749: 'bool0'
    t_750: 'CodeSet'
    t_753: 'bool0'
    t_754: 'Or'
    t_757: 'bool0'
    t_758: 'Repeat'
    t_761: 'bool0'
    t_762: 'Sequence'
    try:
      cast_by_type15(regex__233, Capture)
      t_737 = True
    except Exception9:
      t_737 = False
    with Label11() as s__1230_1231:
      if t_737:
        try:
          t_738 = cast_by_type15(regex__233, Capture)
        except Exception9:
          s__1230_1231.break_()
        this__31.pushCapture__235(t_738)
      else:
        try:
          cast_by_type15(regex__233, CodePoints)
          t_741 = True
        except Exception9:
          t_741 = False
        if t_741:
          try:
            t_742 = cast_by_type15(regex__233, CodePoints)
          except Exception9:
            s__1230_1231.break_()
          this__31.pushCodePoints__251(t_742, False)
        else:
          try:
            cast_by_type15(regex__233, CodeRange)
            t_745 = True
          except Exception9:
            t_745 = False
          if t_745:
            try:
              t_746 = cast_by_type15(regex__233, CodeRange)
            except Exception9:
              s__1230_1231.break_()
            this__31.pushCodeRange__256(t_746)
          else:
            try:
              cast_by_type15(regex__233, CodeSet)
              t_749 = True
            except Exception9:
              t_749 = False
            if t_749:
              try:
                t_750 = cast_by_type15(regex__233, CodeSet)
              except Exception9:
                s__1230_1231.break_()
              this__31.pushCodeSet__262(t_750)
            else:
              try:
                cast_by_type15(regex__233, Or)
                t_753 = True
              except Exception9:
                t_753 = False
              if t_753:
                try:
                  t_754 = cast_by_type15(regex__233, Or)
                except Exception9:
                  s__1230_1231.break_()
                this__31.pushOr__274(t_754)
              else:
                try:
                  cast_by_type15(regex__233, Repeat)
                  t_757 = True
                except Exception9:
                  t_757 = False
                if t_757:
                  try:
                    t_758 = cast_by_type15(regex__233, Repeat)
                  except Exception9:
                    s__1230_1231.break_()
                  this__31.pushRepeat__278(t_758)
                else:
                  try:
                    cast_by_type15(regex__233, Sequence)
                    t_761 = True
                  except Exception9:
                    t_761 = False
                  if t_761:
                    try:
                      t_762 = cast_by_type15(regex__233, Sequence)
                    except Exception9:
                      s__1230_1231.break_()
                    this__31.pushSequence__283(t_762)
                  elif generic_eq_1232(regex__233, begin):
                    try:
                      list_builder_add_1210(this__31.out__227, '^')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, dot):
                    try:
                      list_builder_add_1210(this__31.out__227, '.')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, end):
                    try:
                      list_builder_add_1210(this__31.out__227, '$')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, word_boundary):
                    try:
                      list_builder_add_1210(this__31.out__227, '\\b')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, digit):
                    try:
                      list_builder_add_1210(this__31.out__227, '\\d')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, space):
                    try:
                      list_builder_add_1210(this__31.out__227, '\\s')
                    except Exception9:
                      s__1230_1231.break_()
                  elif generic_eq_1232(regex__233, word):
                    try:
                      list_builder_add_1210(this__31.out__227, '\\w')
                    except Exception9:
                      s__1230_1231.break_()
                  else:
                    None
      return
    raise BubbleException12()
  def pushCapture__235(this__32, capture__236: 'Capture') -> 'None':
    t_1104: 'str2'
    t_1105: 'Regex'
    t_732: 'MutableSequence1[str2]'
    list_builder_add_1210(this__32.out__227, '(')
    t_732 = this__32.out__227
    t_1104 = capture__236.name
    regex_formatter_push_capture_name_1233(this__32, t_732, t_1104)
    t_1105 = capture__236.item
    this__32.pushRegex__232(t_1105)
    list_builder_add_1210(this__32.out__227, ')')
  def pushCode__242(this__34, code__243: 'int10', insideCodeSet__244: 'bool0') -> 'None':
    regex_formatter_push_code_to_1234(this__34, this__34.out__227, code__243, insideCodeSet__244)
  def pushCodePoints__251(this__36, codePoints__252: 'CodePoints', insideCodeSet__253: 'bool0') -> 'None':
    t_1093: 'int10'
    t_1094: 'Any8'
    t_1098: 'Any8' = string_code_points_1225(codePoints__252.value)
    slice__255: 'Any8' = t_1098
    while True:
      if not slice__255.is_empty:
        t_1093 = slice__255.read()
        this__36.pushCode__242(t_1093, insideCodeSet__253)
        t_1094 = slice__255.advance(1)
        slice__255 = t_1094
      else:
        break
  def pushCodeRange__256(this__37, codeRange__257: 'CodeRange') -> 'None':
    list_builder_add_1210(this__37.out__227, '[')
    this__37.pushCodeRangeUnwrapped__259(codeRange__257)
    list_builder_add_1210(this__37.out__227, ']')
  def pushCodeRangeUnwrapped__259(this__38, codeRange__260: 'CodeRange') -> 'None':
    t_1088: 'int10'
    t_1086: 'int10' = codeRange__260.min
    this__38.pushCode__242(t_1086, True)
    list_builder_add_1210(this__38.out__227, '-')
    t_1088 = codeRange__260.max
    this__38.pushCode__242(t_1088, True)
  def pushCodeSet__262(this__39, codeSet__263: 'CodeSet') -> 'None':
    t_1082: 'int10'
    t_710: 'bool0'
    t_711: 'CodeSet'
    t_716: 'CodePart'
    adjusted__265: 'Regex' = this__39.adjustCodeSet__267(codeSet__263, regexRefs__117)
    try:
      cast_by_type15(adjusted__265, CodeSet)
      t_710 = True
    except Exception9:
      t_710 = False
    with Label11() as s__1235_1237:
      if t_710:
        with Label11() as s__1236_1238:
          try:
            t_711 = cast_by_type15(adjusted__265, CodeSet)
            list_builder_add_1210(this__39.out__227, '[')
          except Exception9:
            s__1236_1238.break_()
          if t_711.negated:
            try:
              list_builder_add_1210(this__39.out__227, '^')
            except Exception9:
              s__1236_1238.break_()
          else:
            None
          i__266: 'int10' = 0
          while True:
            t_1082 = len_1220(t_711.items)
            if i__266 < t_1082:
              try:
                t_716 = list_get_1221(t_711.items, i__266)
              except Exception9:
                s__1236_1238.break_()
              this__39.pushCodeSetItem__271(t_716)
              i__266 = i__266 + 1
            else:
              break
          try:
            list_builder_add_1210(this__39.out__227, ']')
            s__1235_1237.break_()
          except Exception9:
            pass
        raise BubbleException12()
      this__39.pushRegex__232(adjusted__265)
  def adjustCodeSet__267(this__40, codeSet__268: 'CodeSet', regexRefs__269: 'RegexRefs__19') -> 'Regex':
    return codeSet__268
  def pushCodeSetItem__271(this__41, codePart__272: 'CodePart') -> 'None':
    t_697: 'bool0'
    t_698: 'CodePoints'
    t_701: 'bool0'
    t_702: 'CodeRange'
    t_705: 'bool0'
    t_706: 'SpecialSet'
    try:
      cast_by_type15(codePart__272, CodePoints)
      t_697 = True
    except Exception9:
      t_697 = False
    with Label11() as s__1239_1240:
      if t_697:
        try:
          t_698 = cast_by_type15(codePart__272, CodePoints)
        except Exception9:
          s__1239_1240.break_()
        this__41.pushCodePoints__251(t_698, True)
      else:
        try:
          cast_by_type15(codePart__272, CodeRange)
          t_701 = True
        except Exception9:
          t_701 = False
        if t_701:
          try:
            t_702 = cast_by_type15(codePart__272, CodeRange)
          except Exception9:
            s__1239_1240.break_()
          this__41.pushCodeRangeUnwrapped__259(t_702)
        else:
          try:
            cast_by_type15(codePart__272, SpecialSet)
            t_705 = True
          except Exception9:
            t_705 = False
          if t_705:
            try:
              t_706 = cast_by_type15(codePart__272, SpecialSet)
            except Exception9:
              s__1239_1240.break_()
            this__41.pushRegex__232(t_706)
          else:
            None
      return
    raise BubbleException12()
  def pushOr__274(this__42, or__275: 'Or') -> 'None':
    t_1066: 'int10'
    t_689: 'Regex'
    t_694: 'Regex'
    with Label11() as s__1241_1243:
      if not (not or__275.items):
        with Label11() as s__1242_1244:
          try:
            list_builder_add_1210(this__42.out__227, '(?:')
            t_689 = list_get_1221(or__275.items, 0)
          except Exception9:
            s__1242_1244.break_()
          this__42.pushRegex__232(t_689)
          i__277: 'int10' = 1
          while True:
            t_1066 = len_1220(or__275.items)
            if i__277 < t_1066:
              try:
                list_builder_add_1210(this__42.out__227, '|')
                t_694 = list_get_1221(or__275.items, i__277)
              except Exception9:
                break
              this__42.pushRegex__232(t_694)
              i__277 = i__277 + 1
            else:
              try:
                list_builder_add_1210(this__42.out__227, ')')
              except Exception9:
                s__1242_1244.break_()
              s__1241_1243.break_()
        raise BubbleException12()
  def pushRepeat__278(this__43, repeat__279: 'Repeat') -> 'None':
    t_1056: 'Regex'
    t_676: 'bool0'
    t_677: 'bool0'
    t_678: 'bool0'
    t_681: 'int10'
    t_683: 'MutableSequence1[str2]'
    with Label11() as s__1245_1246:
      min__281: 'int10'
      max__282: 'Union6[int10, None]'
      try:
        list_builder_add_1210(this__43.out__227, '(?:')
        t_1056 = repeat__279.item
        this__43.pushRegex__232(t_1056)
        list_builder_add_1210(this__43.out__227, ')')
        min__281 = repeat__279.min
        max__282 = repeat__279.max
      except Exception9:
        s__1245_1246.break_()
      if min__281 == 0:
        t_676 = max__282 == 1
      else:
        t_676 = False
      if t_676:
        try:
          list_builder_add_1210(this__43.out__227, '?')
        except Exception9:
          s__1245_1246.break_()
      else:
        if min__281 == 0:
          t_677 = max__282 == None
        else:
          t_677 = False
        if t_677:
          try:
            list_builder_add_1210(this__43.out__227, '*')
          except Exception9:
            s__1245_1246.break_()
        else:
          if min__281 == 1:
            t_678 = max__282 == None
          else:
            t_678 = False
          if t_678:
            try:
              list_builder_add_1210(this__43.out__227, '+')
            except Exception9:
              s__1245_1246.break_()
          else:
            try:
              list_builder_add_1210(this__43.out__227, str_cat_1223('{', int_to_string_1224(min__281)))
            except Exception9:
              s__1245_1246.break_()
            if min__281 != max__282:
              try:
                list_builder_add_1210(this__43.out__227, ',')
              except Exception9:
                s__1245_1246.break_()
              if max__282 != None:
                t_683 = this__43.out__227
                try:
                  t_681 = cast_by_test17(max__282, isinstance_int16)
                  list_builder_add_1210(t_683, int_to_string_1224(t_681))
                except Exception9:
                  s__1245_1246.break_()
              else:
                None
            else:
              None
            try:
              list_builder_add_1210(this__43.out__227, '}')
            except Exception9:
              s__1245_1246.break_()
      if repeat__279.reluctant:
        try:
          list_builder_add_1210(this__43.out__227, '?')
        except Exception9:
          s__1245_1246.break_()
      else:
        None
      return
    raise BubbleException12()
  def pushSequence__283(this__44, sequence__284: 'Sequence') -> 'None':
    t_1054: 'int10'
    t_670: 'Regex'
    i__286: 'int10' = 0
    with Label11() as s__1247_1248:
      while True:
        t_1054 = len_1220(sequence__284.items)
        if i__286 < t_1054:
          try:
            t_670 = list_get_1221(sequence__284.items, i__286)
          except Exception9:
            break
          this__44.pushRegex__232(t_670)
          i__286 = i__286 + 1
        else:
          s__1247_1248.break_()
      raise BubbleException12()
  def max_code(this__45, codePart__288: 'CodePart') -> 'Union6[int10, None]':
    return__116: 'Union6[int10, None]'
    t_1032: 'Any8'
    t_1034: 'Any8'
    t_1039: 'Union6[int10, None]'
    t_1042: 'Union6[int10, None]'
    t_1045: 'Union6[int10, None]'
    t_1048: 'Union6[int10, None]'
    t_643: 'bool0'
    t_644: 'CodePoints'
    t_656: 'bool0'
    t_657: 'CodeRange'
    try:
      cast_by_type15(codePart__288, CodePoints)
      t_643 = True
    except Exception9:
      t_643 = False
    with Label11() as s__1249_1250:
      if t_643:
        try:
          t_644 = cast_by_type15(codePart__288, CodePoints)
        except Exception9:
          s__1249_1250.break_()
        value__290: 'str2' = t_644.value
        if not value__290:
          return__116 = None
        else:
          max__291: 'int10' = 0
          t_1032 = string_code_points_1225(value__290)
          slice__292: 'Any8' = t_1032
          while True:
            if not slice__292.is_empty:
              next__293: 'int10' = slice__292.read()
              if next__293 > max__291:
                max__291 = next__293
              else:
                None
              t_1034 = slice__292.advance(1)
              slice__292 = t_1034
            else:
              break
          return__116 = max__291
      else:
        try:
          cast_by_type15(codePart__288, CodeRange)
          t_656 = True
        except Exception9:
          t_656 = False
        if t_656:
          try:
            t_657 = cast_by_type15(codePart__288, CodeRange)
            t_1039 = t_657.max
            return__116 = t_1039
          except Exception9:
            s__1249_1250.break_()
        elif generic_eq_1232(codePart__288, digit):
          t_1042 = string_code_points_1225('9').read()
          try:
            return__116 = t_1042
          except Exception9:
            s__1249_1250.break_()
        elif generic_eq_1232(codePart__288, space):
          t_1045 = string_code_points_1225(' ').read()
          try:
            return__116 = t_1045
          except Exception9:
            s__1249_1250.break_()
        elif generic_eq_1232(codePart__288, word):
          t_1048 = string_code_points_1225('z').read()
          try:
            return__116 = t_1048
          except Exception9:
            s__1249_1250.break_()
        else:
          return__116 = None
      return return__116
    raise BubbleException12()
  def constructor__294(this__98, out: Optional7['MutableSequence1[str2]'] = None) -> 'None':
    out__295: Optional7['MutableSequence1[str2]'] = out
    t_1028: 'MutableSequence1[str2]'
    if out__295 is None:
      t_1028 = list_1215()
      out__295 = t_1028
    this__98.out__227 = out__295
  def __init__(this__98, out: Optional7['MutableSequence1[str2]'] = None) -> None:
    out__295: Optional7['MutableSequence1[str2]'] = out
    this__98.constructor__294(out__295)
class Begin__12(Special):
  __slots__ = ()
  def constructor__138(this__54) -> 'None':
    None
  def __init__(this__54) -> None:
    this__54.constructor__138()
begin: 'Begin__12' = Begin__12()
class Dot__13(Special):
  __slots__ = ()
  def constructor__139(this__56) -> 'None':
    None
  def __init__(this__56) -> None:
    this__56.constructor__139()
dot: 'Dot__13' = Dot__13()
class End__14(Special):
  __slots__ = ()
  def constructor__140(this__58) -> 'None':
    None
  def __init__(this__58) -> None:
    this__58.constructor__140()
end: 'End__14' = End__14()
class WordBoundary__15(Special):
  __slots__ = ()
  def constructor__141(this__60) -> 'None':
    None
  def __init__(this__60) -> None:
    this__60.constructor__141()
word_boundary: 'WordBoundary__15' = WordBoundary__15()
class Digit__16(SpecialSet):
  __slots__ = ()
  def constructor__142(this__62) -> 'None':
    None
  def __init__(this__62) -> None:
    this__62.constructor__142()
digit: 'Digit__16' = Digit__16()
class Space__17(SpecialSet):
  __slots__ = ()
  def constructor__143(this__64) -> 'None':
    None
  def __init__(this__64) -> None:
    this__64.constructor__143()
space: 'Space__17' = Space__17()
class Word__18(SpecialSet):
  __slots__ = ()
  def constructor__144(this__66) -> 'None':
    None
  def __init__(this__66) -> None:
    this__66.constructor__144()
word: 'Word__18' = Word__18()
def entire(item__167: 'Regex') -> 'Regex':
  global begin, end
  return Sequence((begin, item__167, end))
def one_or_more(item__169: 'Regex', reluctant: Optional7['bool0'] = None) -> 'Repeat':
  reluctant__170: Optional7['bool0'] = reluctant
  if reluctant__170 is None:
    reluctant__170 = False
  return Repeat(item__169, 1, None, reluctant__170)
def optional(item__172: 'Regex', reluctant: Optional7['bool0'] = None) -> 'Repeat':
  reluctant__173: Optional7['bool0'] = reluctant
  if reluctant__173 is None:
    reluctant__173 = False
  return Repeat(item__172, 0, 1, reluctant__173)
regexRefs__117: 'RegexRefs__19' = RegexRefs__19()
