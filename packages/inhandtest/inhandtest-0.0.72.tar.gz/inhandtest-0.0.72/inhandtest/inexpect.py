# -*- coding: utf-8 -*-
# @Time    : 2023/8/31 16:02:16
# @Author  : Pane Li
# @File    : in_expect.py
"""
in_expect

"""
import typing


class expect:
    def __init__(self, value, args=None, kwargs=None):
        self._value = value
        self._args = args
        self._kwargs = kwargs

    @staticmethod
    def __dict_flatten(in_dict, dict_out=None) -> list:
        """ 平铺字典，让字典里面的所有key 和 value 转换成列表

        :param in_dict: 输入的字典
        :param dict_out:
        :return: dict
        """
        if dict_out is None:
            dict_out = []

        for k, v in in_dict.items():
            if isinstance(v, dict):
                for k_, v_ in v.items():
                    if {k: {k_: v_}} not in dict_out:
                        dict_out.append({k: {k_: v_}})
                expect.__dict_flatten(in_dict=v, dict_out=dict_out)
            else:
                if {k: v} not in dict_out:
                    dict_out.append({k: v})

        return dict_out

    @staticmethod
    def __dict_to_list(in_dict, list_out=None) -> list:
        """  将字典里面的所有key 和 value 转换成列表

        :param in_dict: 输入的字典
        :param list_out:

        :return: list
        """
        if list_out is None:
            list_out = []
        if in_dict is not None:
            for k, v in in_dict.items():
                list_out.append(k)
                if isinstance(v, dict):
                    expect.__dict_to_list(in_dict=v, list_out=list_out)
                    continue
                list_out.append(v)

        return list_out

    @staticmethod
    def __dict_in(expect_dict: dict, contain: dict, type_='in') -> None:
        """验证字典包含关系

        :param expect_dict: dict {key: value}
        :param contain: dict
        :return: AssertionError
        """
        if expect_dict and contain:
            contain_to = expect.__dict_flatten(contain)  # 平铺字典
            expect_dict_to = expect.__dict_flatten(expect_dict)  # 平铺字典
            if type_ == 'in':
                assert all(ex_ in expect_dict_to for ex_ in contain_to), f'expect {expect_dict} to contain {contain}'
            else:
                assert all(ex_ not in expect_dict_to for ex_ in contain_to), f'expect {expect_dict} to not contain {contain}'

    def to_eq(self, expect_value):
        """Value is equal， 非严格相同， 只要值相等即可，可以是列表也可以是元组和字典等类型
           ex: expect(1).to_eq(1).to_ne(2)
           a = [1, 2, 3]
           expect(a).to_eq([1, 2, 3])
           a = {"a": 1, "b": 2}
           expect(a).to_eq({"a": 1, "b": 2})
        """
        try:
            assert self._value == expect_value, f'expect {self._value} to be {expect_value}'
        except TypeError:
            raise
        return self

    def to_ne(self, expect_value):
        """Value is not equal
           ex: expect(1).to_ne(2).to_eq(1)
        """
        try:
            assert self._value != expect_value, f'expect {self._value} not to be {expect_value}'
        except TypeError:
            raise
        return self

    def to_lt(self, expect_value):
        """Value is less than
           ex: expect(1).to_lt(2).to_gt(0)
        """
        try:
            assert self._value < expect_value, f'expect {self._value} to less than {expect_value}'
        except TypeError:
            raise
        return self

    def to_gt(self, expect_value):
        """Value is more than
           ex: expect(2).to_gt(1).to_lt(3)
        """
        try:
            assert self._value > expect_value, f'expect {self._value} to more than {expect_value}'
        except TypeError:
            raise
        return self

    def to_le(self, expect_value):
        """Value is less than or equal
           ex: expect(1).to_le(1).to_ge(1)
        """
        try:
            assert self._value <= expect_value, f'expect {self._value} to less than or equal {expect_value}'
        except TypeError:
            raise
        return self

    def to_ge(self, expect_value):
        """Value is more than or equal
           ex: expect(1).to_ge(1).to_le(1)
        """
        try:
            assert self._value >= expect_value, f'expect {self._value} to more than or equal {expect_value}'
        except TypeError:
            raise
        return self

    def to_be(self, expect_value):
        """Value is the same, 严格相同
           ex: expect(1).to_be(1).to_not_be(2), expect('1').to_be('1').to_not_be('2')
        """
        try:
            assert self._value is expect_value, f'expect {self._value} to be {expect_value}'
        except TypeError:
            raise
        return self

    def to_be_false(self):
        """Value is False  False|0|''|[]|{}|None|()"""
        try:
            assert not self._value, f'expect {self._value} to be False'
        except TypeError:
            raise
        return self

    def to_be_true(self):
        """Value is True  True|1|'1'|[1]|{"a": 1}|(1, )"""
        try:
            assert self._value, f'expect {self._value} to be True'
        except TypeError:
            raise
        return self

    def to_not_be(self, expect_value):
        """Value is not the same
           ex: expect(1).to_not_be(2).to_be(1), expect('1').to_not_be('2').to_be('1')
        """
        try:
            assert self._value is not expect_value, f'expect {self._value} to be not {expect_value}'
        except TypeError:
            raise
        return self

    def to_be_empty(self):
        """Value is empty  |''|[]|{}|()"""
        try:
            assert len(self._value) == 0, f'expect {self._value} to be empty'
        except TypeError:
            raise
        return self

    def to_contain(self, expect_value):
        """Value contains
        import re
        value = 'Hello, World'
        expect(value).to_contain('Hello')  True
        expect(value).to_contain(['Hello', 'World'])  True
        expect(value).to_contain(re.compile(r'Hello'))  True
        expect(value).to_contain([re.compile(r'Hello'), re.compile(r'World')]  True
        value = [1, 2, 3]
        expect(value).to_contain(1)  True
        expect(value).to_contain([3, 1])  True
        expect(value).to_contain([1, 2, 3])  True
        value = [[1, 2], 3, 4]
        expect(value).to_contain([1, 2])  True
        expect(value).to_contain([[1, 2]]) True
        expect(value).to_contain([[1, 2], 3]) True
        value = {"a": 1, "b": 2, 'c': {"d": 3, "f": 4}, "e": None}
        expect(value).to_contain({"a": 1}) True
        expect(value).to_contain([{"a": 1}, {'c': {"d": 3}}])  True
        expect(value).to_contain({"d": 3}) True
        expect(value).to_contain({"e": None}) True
        expect(value).to_contain({"h": None}) False  # key not exist
        expect(value).to_contain("a")  True
        expect(value).to_contain(None)  True
        expect(value).to_contain(["a", "f", "4", None])  True
        """
        try:
            if isinstance(expect_value, typing.Pattern):
                assert expect_value.search(self._value), f'expect {self._value} to contain {expect_value}'
            elif isinstance(expect_value, dict):
                if isinstance(self._value, dict):
                    expect.__dict_in(self._value, expect_value)
                else:
                    assert expect_value in self._value, f'expect {self._value} to contain {expect_value}'
            elif isinstance(expect_value, (list, tuple, set)):
                try:
                    if expect_value in self._value:
                        pass
                    else:
                        for expect_ in expect_value:
                            if isinstance(expect_, typing.Pattern):
                                assert expect_.search(self._value), f'expect {self._value} to contain {expect_}'
                            elif isinstance(expect_, dict):
                                if isinstance(self._value, dict):
                                    expect.__dict_in(self._value, expect_)
                                else:
                                    assert expect_ in self._value, f'expect {self._value} to contain {expect_}'
                            else:
                                if isinstance(self._value, dict):
                                    assert expect_ in self.__dict_to_list(
                                        self._value), f'expect {self._value} to contain {expect_}'
                                else:
                                    assert expect_ in self._value, f'expect {self._value} to contain {expect_}'
                except:
                    for expect_ in expect_value:
                        if isinstance(expect_, typing.Pattern):
                            assert expect_.search(self._value), f'expect {self._value} to contain {expect_}'
                        elif isinstance(expect_, dict):
                            if isinstance(self._value, dict):
                                expect.__dict_in(self._value, expect_)
                            else:
                                assert expect_ in self._value, f'expect {self._value} to contain {expect_}'
                        else:
                            if isinstance(self._value, dict):
                                assert expect_ in self.__dict_to_list(
                                    self._value), f'expect {self._value} to contain {expect_}'
                            else:
                                assert expect_ in self._value, f'expect {self._value} to contain {expect_}'
            else:
                if isinstance(self._value, dict):
                    assert expect_value in self.__dict_to_list(
                        self._value), f'expect {self._value} to contain {expect_value}'
                else:
                    assert expect_value in self._value, f'expect {self._value} to contain {expect_value}'
        except TypeError:
            raise
        return self

    def to_not_contain(self, expect_value):
        """Value not contains
        import re
        value = 'Hello, World'
        expect(value).to_not_contain('Hello1')  True
        expect(value).to_not_contain(['Hello1', 'World1'])  True
        expect(value).to_not_contain(re.compile(r'Hello1'))  True
        expect(value).to_not_contain([re.compile(r'Hello1'), re.compile(r'World1')])  True
        value = [1, 2, 3]
        expect(value).to_not_contain(4)  True
        expect(value).to_not_contain([4, 5])  True
        value = [[1, 2], 3, 4]
        expect(value).to_not_contain([1, 5])  True
        expect(value).to_not_contain([[1, 5]]) True
        expect(value).to_not_contain([[1, 5], 5])  True
        value = {"a": 1, "b": 2, 'c': {"d": 3}, "e": None}
        expect(value).to_not_contain({"a": 2}) True
        expect(value).to_not_contain([{"a": 2}, {'c': {"d": 4}}]) True
        expect(value).to_not_contain({"d": 4}) True
        expect(value).to_not_contain({"h": None}) True
        expect(value).to_not_contain({"e": None}) False
        expect(value).to_not_contain("a")  False
        expect(value).to_not_contain(None)  False
        expect(value).to_not_contain(["a", "d", 3, None])  False
        """
        try:
            if isinstance(expect_value, typing.Pattern):
                assert not expect_value.search(self._value), f'expect {self._value} to not contain {expect_value}'
            elif isinstance(expect_value, dict):
                if isinstance(self._value, dict):
                    expect.__dict_in(self._value, expect_value, 'not_in')
                else:
                    assert expect_value not in self._value, f'expect {self._value} to not contain {expect_value}'
            elif isinstance(expect_value, (list, tuple, set)):
                try:
                    if expect_value in self._value:
                        raise AssertionError(f'expect {self._value} to not contain {expect_value}')
                    else:
                        for expect_ in expect_value:
                            if isinstance(expect_, typing.Pattern):
                                assert not expect_.search(
                                    self._value), f'expect {self._value} to not contain {expect_}'
                            elif isinstance(expect_, dict):
                                if isinstance(self._value, dict):
                                    expect.__dict_in(self._value, expect_, 'not_in')
                                else:
                                    assert expect_ not in self._value, f'expect {self._value} to not contain {expect_}'
                            else:
                                if isinstance(self._value, dict):
                                    assert expect_ not in self.__dict_to_list(
                                        self._value), f'expect {self._value} to not contain {expect_}'
                                else:
                                    assert expect_ not in self._value, f'expect {self._value} to not contain {expect_}'
                except TypeError:
                    for expect_ in expect_value:
                        if isinstance(expect_, typing.Pattern):
                            assert not expect_.search(
                                self._value), f'expect {self._value} to not contain {expect_}'
                        elif isinstance(expect_, dict):
                            if isinstance(self._value, dict):
                                expect.__dict_in(self._value, expect_, 'not_in')
                            else:
                                assert expect_ not in self._value, f'expect {self._value} to not contain {expect_}'
                        else:
                            if isinstance(self._value, dict):
                                assert expect_ not in self.__dict_to_list(
                                    self._value), f'expect {self._value} to not contain {expect_}'
                            else:
                                assert expect_ not in self._value, f'expect {self._value} to not contain {expect_}'
            else:
                if isinstance(self._value, dict):
                    assert expect_value not in self.__dict_to_list(
                        self._value), f'expect {self._value} to not contain {expect_value}'
                else:
                    assert expect_value not in self._value, f'expect {self._value} to not contain {expect_value}'
        except TypeError:
            raise
        return self

    def to_have_length(self, expect_value):
        """Array or string has length
           ex: expect('Hello, World').toHaveLength(12)
           expect([1, 2, 3]).toHaveLength(3)
        """
        try:
            assert len(self._value) == expect_value, f'expect {self._value} to have length {expect_value}'
        except TypeError:
            raise
        return self

    def to_have_property(self, expect_key: str, expect_value: typing.Any = None):
        """dict has a property  or list contain dict has a property
            ex:
            value = {a: {b: [42]}, c: True}
            expect(value).to_have_property('a.b')
            expect(value).to_have_property('a.b', [42])
            expect(value).to_have_property('a.b[0]', 42)
            expect(value).to_have_property('c')
            expect(value).toHaveProperty('c', True)
            value = [{a: 1}, {a: 2}]
            expect(value).to_have_property('[0].a', 1)
        """
        try:
            keys = expect_key.split('.')
            expression = 'self._value'
            for key in keys:
                if key.startswith('['):
                    expression += f'{key}'
                else:
                    key_ = key.split('[', 1)[0]
                    try:
                        key_list = key.split('[', 1)[1]
                        expression += f'.get("{key_}")[{key_list}'
                    except IndexError:
                        expression += f'.get("{key_}")'
            now_value = eval(expression, {'self': self})
            if expect_value is None:
                assert now_value is not None, f'expect {self._value} to have property {expect_key}'
            else:
                if isinstance(now_value, bool) or isinstance(expect_value, bool):
                    assert eval(expression, {'self': self}) is expect_value, \
                        f'expect {self._value} to have property {expect_key} is {expect_value}'
                else:
                    assert eval(expression, {'self': self}) == expect_value, \
                        f'expect {self._value} to have property {expect_key} is {expect_value}'
        except TypeError:
            raise
        return self

    def to_match(self, expect_value: str or typing.Pattern):
        """string value matches a regular expression
           ex:
           expect('Hello, World').to_match(r'Hello')
           expect('Hello, World').to_match(re.compile(r'^Hello.*'))
        """
        import re
        try:
            assert re.match(expect_value, self._value), f'expect {self._value} to match {expect_value}'
        except TypeError:
            raise
        return self

    def to_be_instance_of(self, expect_value):
        """Value is instance of
            ex:
            value = [1, 2, 3]
            expect(value).to_be_instance_of(list)
        """
        try:
            assert isinstance(self._value, expect_value), f'expect {self._value} to be instance of {expect_value}'
        except TypeError:
            raise
        return self


class raises:

    def __init__(self, expected_exception, match=None):
        if not issubclass(expected_exception, BaseException):
            raise TypeError(f"expected_exception must be classes, not {expected_exception.__name__}")
        if not isinstance(match, (str, typing.Pattern, type(None))):
            raise TypeError(f"match must be str or typing.Pattern")
        self.expected_exception = expected_exception
        self.match = match

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            if not issubclass(exc_type, self.expected_exception):
                return False
            if self.match is not None:
                if isinstance(self.match, str):
                    if self.match not in str(exc_value):
                        return False
                else:
                    if not self.match.search(str(exc_value)):
                        return False
            # 返回True表示异常已被处理，否则异常将继续传播
            return True
        else:
            raise Exception(f"DID NOT RAISE {self.expected_exception.__name__}")


if __name__ == '__main__':
    import re

    # value = {"k1": '123', 'k2': {"k2-1": None, "k2-2": {"k3": 1}}, 'k4': [123]}
    # expect(value).to_not_contain({'k2': {"k2-1": 123, "k2-2": {"k3": 3}}})
    # expect(value).to_contain({"k1": '123'})
