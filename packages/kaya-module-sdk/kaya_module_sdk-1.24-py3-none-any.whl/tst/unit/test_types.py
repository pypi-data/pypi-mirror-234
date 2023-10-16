import unittest
import time

from kaya_module_sdk.sdk import KTimeSeries, KList, KString, KInt, KFloat


class TestDataTypeTimeSeries(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n[ TestSuit ]: Kaya Module SDK Data Types\n')
        cls.string_time_series = KTimeSeries({'a': 1.0, 'b': 2.0, 'c': 3.0})    # TimeSeries[str]
        cls.int_time_series = KTimeSeries({1: 10.0, 2: 20.0, 3: 30.0})          # TimeSeries[int]
        cls.float_time_series = KTimeSeries({0.5: 1.0, 1.5: 2.0})               # TimeSeries[float]
        cls.bool_time_series = KTimeSeries({True: 1.0, False: 2.0})             # TimeSeries[bool]
        cls.string_list = KList(['a', 'b', 'c'])                                # List[str]
        cls.int_list = KList([1, 2, 3])                                         # List[int]
        cls.float_list = KList([1.1, 2.2, 3.3])                                 # List[float]
        cls.bool_list = KList([True, False, True])                              # List[bool]
        cls.dummy_int = KInt(5)
        cls.dummy_float = KFloat(2.5)
        cls.dummy_string = KString('Special K is for Kaya')
        cls.time_series_list = KList([
            cls.string_time_series, cls.int_time_series, cls.float_time_series
        ])                                                                     # List[TimeSeries]

    @classmethod
    def tearDownClass(cls):
        print('\n[ DONE ]: Kaya Module SDK Data Types')
        del cls.string_time_series
        del cls.int_time_series
        del cls.float_time_series
        del cls.bool_time_series
        del cls.dummy_int
        del cls.dummy_float
        del cls.dummy_string

    # Test cases

    def test_int_data_type(self):
        print(
            '\n[ TEST ]: KInt...\n{}\n'.format(self.dummy_int)
        )
        add = self.dummy_int + 2
        self.assertEqual(add, 7)
        subtract = self.dummy_int - 2
        self.assertEqual(subtract, 3)
        multiply = self.dummy_int * 2
        self.assertEqual(multiply, 10)
        divide = self.dummy_int / 2
        self.assertEqual(divide, 2.5)
        remainder = self.dummy_int % 2
        self.assertEqual(remainder, 1)

        add = self.dummy_int + KInt(2)
        self.assertEqual(add, 7)
        subtract = self.dummy_int - KInt(2)
        self.assertEqual(subtract, 3)
        multiply = self.dummy_int * KInt(2)
        self.assertEqual(multiply, 10)
        divide = self.dummy_int / KInt(2)
        self.assertEqual(divide, 2.5)
        remainder = self.dummy_int % KInt(2)
        self.assertEqual(remainder, 1)

    def test_float_data_type(self):
        print(
            '\n[ TEST ]: KFloat...\n{}\n'.format(self.dummy_float)
        )
        add = self.dummy_float + 2
        self.assertEqual(add, 4.5)
        subtract = self.dummy_float - 2
        self.assertEqual(subtract, 0.5)
        multiply = self.dummy_float * 2
        self.assertEqual(multiply, 5.0)
        divide = self.dummy_float / 2
        self.assertEqual(divide, 1.25)
        remainder = self.dummy_float % 2
        self.assertEqual(remainder, 0.5)

        add = self.dummy_float + KFloat(2.0)
        self.assertEqual(add, 4.5)
        subtract = self.dummy_float - KFloat(2.0)
        self.assertEqual(subtract, 0.5)
        multiply = self.dummy_float * KFloat(2.0)
        self.assertEqual(multiply, 5.0)
        divide = self.dummy_float / KFloat(2.0)
        self.assertEqual(divide, 1.25)
        remainder = self.dummy_float % KFloat(2.0)
        self.assertEqual(remainder, 0.5)

    def test_string_data_type(self):
        print(
            '\n[ TEST ]: KString...\n{}\n'.format(self.dummy_string)
        )

        self.assertEqual(len(self.dummy_string), 21)
        self.assertEqual(len(self.dummy_string.split(' ')), 5)

        concat = self.dummy_string + ' another one'
        self.assertEqual(len(concat.split(' ')), 7)

        concat = self.dummy_string + KString(' another one')
        self.assertEqual(len(concat.split(' ')), 7)

    def test_string_list_data_type(self):
        print(
            '\n[ TEST ]: KList[str]...\n{}\n'.format(self.string_list)
        )
        self.string_list.append('d')
        self.assertEqual(len(self.string_list), 4)

        self.string_list.extend(['e', 'f', 'g'])
        self.assertEqual(len(self.string_list), 7)

        self.string_list.insert(0, 'x')
        self.assertEqual(self.string_list[0], 'x')

        self.string_list.remove('x')
        self.assertNotEqual(self.string_list[0], 'x')

        value = self.string_list.pop(0)
        self.assertEqual(len(self.string_list), 6)
        self.assertTrue(isinstance(value, str))

        index = self.string_list.index('f', end=len(self.string_list))
        self.assertTrue(isinstance(index, int))

        no_of_appearances = self.string_list.count('f')
        self.assertTrue(isinstance(no_of_appearances, int))

    def test_int_list_data_type(self):
        print(
            '\n[ TEST ]: KList[int]...\n{}\n'.format(self.int_list)
        )
        self.int_list.append(4)
        self.assertEqual(len(self.int_list), 4)

        self.int_list.extend([5, 6, 7])
        self.assertEqual(len(self.int_list), 7)

        self.int_list.insert(0, 9)
        self.assertEqual(self.int_list[0], 9)

        self.int_list.remove(9)
        self.assertNotEqual(self.int_list[0], 9)

        value = self.int_list.pop(0)
        self.assertEqual(len(self.int_list), 6)
        self.assertTrue(isinstance(value, int))

        index = self.int_list.index(5, end=len(self.int_list))
        self.assertTrue(isinstance(index, int))

        no_of_appearances = self.int_list.count(5)
        self.assertTrue(isinstance(no_of_appearances, int))

    def test_float_list_data_type(self):
        print(
            '\n[ TEST ]: KList[float]...\n{}\n'.format(self.float_list)
        )
        self.float_list.append(4.4)
        self.assertEqual(len(self.float_list), 4)

        self.float_list.extend([5.5, 6.6, 7.7])
        self.assertEqual(len(self.float_list), 7)

        self.float_list.insert(0, 99.99)
        self.assertEqual(self.float_list[0], 99.99)

        self.float_list.remove(99.99)
        self.assertNotEqual(self.float_list[0], 99.99)

        value = self.float_list.pop(0)
        self.assertEqual(len(self.float_list), 6)
        self.assertTrue(isinstance(value, float))

        index = self.float_list.index(5.5, end=len(self.float_list))
        self.assertTrue(isinstance(index, int))

        no_of_appearances = self.float_list.count(5.5)
        self.assertTrue(isinstance(no_of_appearances, int))

    def test_bool_list_data_type(self):
        print(
            '\n[ TEST ]: KList[bool]...\n{}\n'.format(self.bool_list)
        )
        self.bool_list.append(False)
        self.assertEqual(len(self.bool_list), 4)

        self.bool_list.extend([True, False, True])
        self.assertEqual(len(self.bool_list), 7)

        value = self.bool_list.pop(0)
        self.assertEqual(len(self.bool_list), 6)
        self.assertTrue(isinstance(value, bool))

        self.bool_list.insert(0, True)
        self.assertEqual(self.bool_list[0], True)

        index = self.bool_list.index(True, end=len(self.bool_list))
        self.assertTrue(isinstance(index, int))

        no_of_appearances = self.bool_list.count(True)
        self.assertTrue(isinstance(no_of_appearances, int))

        self.bool_list.remove(True)
        self.assertNotEqual(self.bool_list[0], True)

    def test_time_series_list_data_type(self):
        print(
            '\n[ TEST ]: KList[TimeSeries]...\n{}\n'.format(self.time_series_list)
        )
        self.time_series_list.append(self.bool_time_series)
        self.assertEqual(len(self.time_series_list), 4)

        self.time_series_list.remove(self.bool_time_series)
        self.assertEqual(len(self.time_series_list), 3)

        self.time_series_list.extend([self.bool_time_series, ])
        self.assertEqual(len(self.time_series_list), 4)

        value = self.time_series_list.pop(3)
        self.assertEqual(len(self.time_series_list), 3)
        self.assertTrue(isinstance(value, KTimeSeries))

        self.time_series_list.insert(0, self.bool_time_series)
        self.assertEqual(self.time_series_list[0], self.bool_time_series)

        index = self.time_series_list.index(
            self.bool_time_series, end=len(self.time_series_list)
        )
        self.assertTrue(isinstance(index, int))
        self.assertEqual(index, 0)

        no_of_appearances = self.time_series_list.count(self.bool_time_series)
        self.assertTrue(isinstance(no_of_appearances, int))

    def test_string_time_series_data_type(self):
        print(
            '\n[ TEST ]: KTimeSeries[str]...\n{}\n'.format(self.string_time_series)
        )

        length = len(self.string_time_series)
        self.assertEqual(length, 3)

        list_of_keys = list(self.string_time_series.keys())
        self.assertEqual(len(list_of_keys), 3)

        list_of_tuple_pairs = list(self.string_time_series.items())
        self.assertEqual(len(list_of_tuple_pairs), 3)
        self.string_time_series['a'] = 12345
        self.assertEqual(self.string_time_series['a'], 12345)

    def test_int_time_series_data_type(self):
        print(
            '\n[ TEST ]: KTimeSeries[int]...\n{}\n'.format(self.int_time_series)
        )

        length = len(self.int_time_series)
        self.assertEqual(length, 3)

        list_of_keys = list(self.int_time_series.keys())
        self.assertEqual(len(list_of_keys), 3)

        list_of_tuple_pairs = list(self.int_time_series.items())
        self.assertEqual(len(list_of_tuple_pairs), 3)
        self.int_time_series[1] = 12345
        self.assertEqual(self.int_time_series[1], 12345)

    def test_float_time_series_data_type(self):
        print(
            '\n[ TEST ]: KTimeSeries[float]...\n{}\n'.format(self.float_time_series)
        )

        length = len(self.float_time_series)
        self.assertEqual(length, 2)

        list_of_keys = list(self.float_time_series.keys())
        self.assertEqual(len(list_of_keys), 2)

        list_of_tuple_pairs = list(self.float_time_series.items())
        self.assertEqual(len(list_of_tuple_pairs), 2)
        self.float_time_series[0.5] = 12345.12345
        self.assertEqual(self.float_time_series[0.5], 12345.12345)

    def test_bool_time_series_data_type(self):
        print(
            '\n[ TEST ]: KTimeSeries[bool]...\n{}\n'.format(self.bool_time_series)
        )

        length = len(self.bool_time_series)
        self.assertEqual(length, 2)

        list_of_keys = list(self.bool_time_series.keys())
        self.assertEqual(len(list_of_keys), 2)

        list_of_tuple_pairs = list(self.bool_time_series.items())
        self.assertEqual(len(list_of_tuple_pairs), 2)
        self.bool_time_series[True] = 12345
        self.assertEqual(self.bool_time_series[True], 12345)


