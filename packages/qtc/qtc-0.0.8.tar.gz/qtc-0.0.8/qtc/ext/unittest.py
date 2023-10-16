import os
import pandas as pd
import unittest
import typing as T
from qtc.ext.inspect import inspect_caller


class TestCase(unittest.TestCase):
    # def setUp(self):
    #     def dataframe_equals(df1, df2, msg=None):
    #         return df1.equals(df2)
    #     #
    #
    #     def index_equals(index1, index2, msg=None):
    #         return index1.equals(index2)
    #     #
    #     self.addTypeEqualityFunc(pd.DataFrame, dataframe_equals)
    #     self.addTypeEqualityFunc(pd.Index, index_equals)
    # #

    @staticmethod
    def load_benchmark(basename: str,
                       parse_dates: T.Optional[str] = None):
        caller_info = inspect_caller(skip=2, return_info=['FILENAME'])
        caller_file = os.path.realpath(caller_info['FILENAME'])

        benchmark_file = os.path.join(os.path.dirname(caller_file), 'benchmark', basename)
        benchmark = pd.read_csv(benchmark_file, sep=',', parse_dates=parse_dates)
        return benchmark


def main():
    unittest.main()
