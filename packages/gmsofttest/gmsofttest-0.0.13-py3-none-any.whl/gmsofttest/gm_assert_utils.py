"""
Name : gm_assert_utils.py
Author  : 写上自己的名字
Contact : 邮箱地址
Time    : 2023-05-20 16:46
Desc: 验证assert封装
"""
import pytest

EQUALTYPENOTICE = "两个值不相等，注意类型是否一致！！！"
NOTEQUALTYPENOTICE = "两个值相等，注意类型是否一致！！！"
INCLUDENOTICE = "第一个值不在第二个值内，请检查！"
NOINCLUDENOTICE = "第一个值在第二个值内，请检查！"
CODENOTICE = "请求期望CODE与返回CODE不一致，请检查！"

def gm_assert_equal(first_value, second_value, types):
    """验证是否相等"""
    try:
        first = _convert_type(first_value, to_type=types)
        second = _convert_type(second_value, to_type=types)
        assert first == second, EQUALTYPENOTICE
    except AssertionError as e:
        raise AssertionError(e)

def gm_assert_in(first_value, second_value, types):
    """验证第一个值包含在第二个值内"""
    try:
        first = _convert_type(first_value, to_type=types)
        second = _convert_type(second_value, to_type=types)
        print(first)
        print(second)
        print(first in second)
        assert first in second, INCLUDENOTICE
    except AssertionError as e:
        raise AssertionError(e)

def gm_assert_not_in(first_value, second_value, types):
    """验证第一个值不包含在第二个值内"""
    try:
        first = _convert_type(first_value, to_type=types)
        second = _convert_type(second_value, to_type=types)
        assert first not in second, NOINCLUDENOTICE
    except AssertionError as e:
        raise AssertionError(e)

def gm_assert_not_equal(first_value, second_value, types):
    """验证不相等"""
    try:
        first = _convert_type(first_value, to_type=types)
        second = _convert_type(second_value, to_type=types)
        assert first != second, NOTEQUALTYPENOTICE
    except AssertionError as e:
        raise AssertionError(e)

def gm_assert_response_code(first_value, second_value, types):
    """验证response的code值"""
    try:
        first = _convert_type(first_value, to_type=types)
        second = _convert_type(second_value, to_type=types)
        print('多数据验证')
        assert first == second, CODENOTICE
    except AssertionError as e:
        raise AssertionError(e)

def gm_assert_multiple_values_equal(values):
    """多数据验证相等"""
    assert len(values) > 1, "At least two values are needed"
    for i in range(0, len(values)):
        values[i] = _convert_type(values[i])
        print(values[i])
        assert values[i] == values[0], f"第{i+1}个数的Value {values[i]} does not equal {values[0]}"

def gm_assert_lists_iseuqals(list1, list2):
    """验证两个列表的长度是否相等，并分别对比两个列表相同Index的值是否相等"""
    assert len(list1) == len(list2)
    for i in range(len(list1)):
        print(list1[i], list2[i])
        assert list1[i] == list2[i], f"列表List1的第{i+1}个数的Value {list1[i]} != 列表List2的第{i+1}个数的Value {list2[i]}"

def gm_assert_lists_isinclude(list1, list2, reverse=False):
    """验证列表的值是否在另一列表"""
    if reverse is False:
        for i in range(len(list2)):
            print(list2[i])
            assert list2[i] in list1, f"列表2的第{i + 1}个数的值：{list2[i]}   在列表1不存在"
    else:
        for i in range(len(list1)):
            assert list1[i] in list2, f"列表1的第{i + 1}个数的值：{list1[i]}   在列表2不存在"

def _convert_type(value, to_type=str, default=None):
    try:
        return to_type(value)
    except (ValueError, TypeError):
        return default

def gm_assert_dict_iseuqal(dict1, dict2):
    """验证两个字典的长度是否相等，并分别对比两个字典相同Index的值是否相等"""
    print(len(dict1))
    print(len(dict2))
    assert len(dict1) == len(dict2)
    for k in dict1.keys():
        print(dict1[k], dict2[k])
        assert str(dict1[k]) == str(dict2[k]), f"字典1的键{k}的Value {dict1[k]} != 字典2的键{k}的Value {dict2[k]}"


if __name__ == '__main__':
    first_value = {'id': '204113', 'orgname': '大家软件'}
    second_value = {'id': 204113, 'orgname': '大家软件'}
    print(type(first_value))
    print(type(second_value))
    gm_assert_dict_iseuqal(first_value, second_value)


    # gm_assert_multiple_values_equal([3, 3, '3'], int)
    # first_value = 'ok'
    # # second_value = '{"code":20000,"message":"ok","description":"","data":{"todoRationalNum":18,"todoAuditNum":1,"todoEleGuaranteeNum":1,"todoAbolishEleGuaranteeNum":0}}'
    # types = 'str'
    # second_value = 'okok'
    # # gm_assert_in(first_value,second_value, types)
    # # print(second_value)
    # # print(type(second_value))
    # gm_assert_equal('str', 'str1', str)

