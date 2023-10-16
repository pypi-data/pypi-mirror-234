from builtins import bool as bool0, str as str2, Exception as Exception9, int as int10, tuple as tuple_1212, list as list_1215, len as len_1220
from typing import MutableSequence as MutableSequence1, Callable as Callable3, Sequence as Sequence5, Union as Union6, Optional as Optional7, Any as Any8
from pytest import fail as fail4
from temper_core import Pair as Pair_1216, Label as Label11, BubbleException as BubbleException12, list_builder_add as list_builder_add_1210, list_join as list_join_1214, list_map as list_map_1217, list_get as list_get_1221, str_cat as str_cat_1223
from temper_core import LoggingConsole
vGlobalConsole__45_1222 = LoggingConsole(__name__)
class Test:
  passing__16: 'bool0'
  failedOnAssert__17: 'bool0'
  hasUnhandledFail__18: 'bool0'
  _failedOnAssert__58: 'bool0'
  _passing__59: 'bool0'
  _messages__60: 'MutableSequence1[str2]'
  __slots__ = ('passing__16', 'failedOnAssert__17', 'hasUnhandledFail__18', '_failedOnAssert__58', '_passing__59', '_messages__60')
  def assert_(this__7, success__36: 'bool0', message__37: 'Callable3[[], str2]') -> 'None':
    if not success__36:
      this__7._passing__59 = False
      list_builder_add_1210(this__7._messages__60, message__37())
    else:
      None
  def assert_hard(this__8, success__40: 'bool0', message__41: 'Callable3[[], str2]') -> 'None':
    this__8.assert_(success__40, message__41)
    if not success__40:
      this__8._failedOnAssert__58 = True
      fail4(str2(this__8.messages_combined()))
    else:
      None
  def soft_fail_to_hard(this__9) -> 'None':
    if this__9.has_unhandled_fail:
      this__9._failedOnAssert__58 = True
      fail4(str2(this__9.messages_combined()))
    else:
      None
  @property
  def passing(this__11) -> 'bool0':
    return this__11._passing__59
  def messages(this__12) -> 'Sequence5[str2]':
    return tuple_1212(this__12._messages__60)
  @property
  def failed_on_assert(this__13) -> 'bool0':
    return this__13._failedOnAssert__58
  @property
  def has_unhandled_fail(this__14) -> 'bool0':
    t_184: 'bool0'
    if this__14._failedOnAssert__58:
      t_184 = True
    else:
      t_184 = this__14._passing__59
    return not t_184
  def messages_combined(this__15) -> 'Union6[str2, None]':
    return__30: 'Union6[str2, None]'
    t_287: 'MutableSequence1[str2]'
    t_288: 'Union6[str2, None]'
    if not this__15._messages__60:
      return__30 = None
    else:
      t_287 = this__15._messages__60
      def fn__284(it__57: 'str2') -> 'str2':
        return it__57
      t_288 = list_join_1214(t_287, ', ', fn__284)
      return__30 = t_288
    return return__30
  def constructor__61(this__19, failed_on_assert: Optional7['bool0'] = None, passing: Optional7['bool0'] = None, messages: Optional7['MutableSequence1[str2]'] = None) -> 'None':
    _failedOnAssert__62: Optional7['bool0'] = failed_on_assert
    _passing__63: Optional7['bool0'] = passing
    _messages__64: Optional7['MutableSequence1[str2]'] = messages
    t_281: 'MutableSequence1[str2]'
    if _failedOnAssert__62 is None:
      _failedOnAssert__62 = False
    if _passing__63 is None:
      _passing__63 = True
    if _messages__64 is None:
      t_281 = list_1215()
      _messages__64 = t_281
    this__19._failedOnAssert__58 = _failedOnAssert__62
    this__19._passing__59 = _passing__63
    this__19._messages__60 = _messages__64
  def __init__(this__19, failed_on_assert: Optional7['bool0'] = None, passing: Optional7['bool0'] = None, messages: Optional7['MutableSequence1[str2]'] = None) -> None:
    _failedOnAssert__62: Optional7['bool0'] = failed_on_assert
    _passing__63: Optional7['bool0'] = passing
    _messages__64: Optional7['MutableSequence1[str2]'] = messages
    this__19.constructor__61(_failedOnAssert__62, _passing__63, _messages__64)
test_name: 'Any8' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: String: Type>>', NotImplemented)[1]
test_fun: 'Any8' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: fn (Test): (Void | Bubble): Type>>', NotImplemented)[1]
test_case: 'Any8' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: Pair<String, fn (Test): (Void | Bubble)>: Type>>', NotImplemented)[1]
test_failure_message: 'Any8' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: String: Type>>', NotImplemented)[1]
test_result: 'Any8' = ('<<lang.temper.value.TType: Type, lang.temper.value.Value: Pair<String, List<String>>: Type>>', NotImplemented)[1]
def process_test_cases(testCases__65: 'Sequence5[(Pair_1216[str2, (Callable3[[Test], None])])]') -> 'Sequence5[(Pair_1216[str2, (Sequence5[str2])])]':
  global list_map_1217
  def fn__274(testCase__67: 'Pair_1216[str2, (Callable3[[Test], None])]') -> 'Pair_1216[str2, (Sequence5[str2])]':
    global Pair_1216, list_1215, list_builder_add_1210, tuple_1212
    t_265: 'bool0'
    t_267: 'Sequence5[str2]'
    t_166: 'bool0'
    key__69: 'str2' = testCase__67.key
    fun__70: 'Callable3[[Test], None]' = testCase__67.value
    test__71: 'Test' = Test()
    hadBubble__72: 'bool0'
    try:
      fun__70(test__71)
      hadBubble__72 = False
    except Exception9:
      hadBubble__72 = True
    messages__73: 'Sequence5[str2]' = test__71.messages()
    failures__74: 'Sequence5[str2]'
    if test__71.passing:
      failures__74 = ()
    else:
      if hadBubble__72:
        t_265 = test__71.failed_on_assert
        t_166 = not t_265
      else:
        t_166 = False
      if t_166:
        allMessages__75: 'MutableSequence1[str2]' = list_1215(messages__73)
        list_builder_add_1210(allMessages__75, 'Bubble')
        t_267 = tuple_1212(allMessages__75)
        failures__74 = t_267
      else:
        failures__74 = messages__73
    return Pair_1216(key__69, failures__74)
  return list_map_1217(testCases__65, fn__274)
def report_test_results(testResults__76: 'Sequence5[(Pair_1216[str2, (Sequence5[str2])])]') -> 'None':
  global len_1220, list_get_1221, list_join_1214, str_cat_1223, vGlobalConsole__45_1222
  t_252: 'int10'
  t_152: 'Pair_1216[str2, (Sequence5[str2])]'
  i__78: 'int10' = 0
  with Label11() as s__1218_1219:
    while True:
      t_252 = len_1220(testResults__76)
      if i__78 < t_252:
        try:
          t_152 = list_get_1221(testResults__76, i__78)
        except Exception9:
          break
        testResult__79: 'Pair_1216[str2, (Sequence5[str2])]' = t_152
        failureMessages__80: 'Sequence5[str2]' = testResult__79.value
        if not failureMessages__80:
          vGlobalConsole__45_1222.log(str_cat_1223(testResult__79.key, ': Passed'))
        else:
          def fn__250(it__82: 'str2') -> 'str2':
            return it__82
          message__81: 'str2' = list_join_1214(failureMessages__80, ', ', fn__250)
          vGlobalConsole__45_1222.log(str_cat_1223(testResult__79.key, ': Failed ', message__81))
        i__78 = i__78 + 1
      else:
        s__1218_1219.break_()
    raise BubbleException12()
def run_test_cases(testCases__83: 'Sequence5[(Pair_1216[str2, (Callable3[[Test], None])])]') -> 'None':
  global process_test_cases, report_test_results
  report_test_results(process_test_cases(testCases__83))
def run_test(testFun__85: 'Callable3[[Test], None]') -> 'None':
  test__87: 'Test' = Test()
  testFun__85(test__87)
  test__87.soft_fail_to_hard()
