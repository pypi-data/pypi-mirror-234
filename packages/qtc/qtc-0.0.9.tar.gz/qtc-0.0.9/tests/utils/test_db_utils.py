import qtc.ext.unittest as ut
import qtc.utils.db_utils as dbu
from qtc.consts.enums import DBType
import pandas as pd


class TestDBUtils(ut.TestCase):
    def test__infer_db_type_name(self):
        self.assertEqual(dbu._infer_db_type_name(db_code='GMBP-RDS'), (DBType.MYSQL, 'GMBP-RDS'))

    def test__process_cols(self):
        self.assertEqual(dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return',
                                           required_cols='SecurityId,NMV,BbergCode'),
                         ['SecurityId', 'NMV', 'BbergCode', 'AxiomaId', 'Return'])
        self.assertEqual(dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return',
                                           required_cols='SecurityId'),
                         ['SecurityId', 'AxiomaId', 'BbergCode', 'NMV', 'Return'])
        self.assertEqual(dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return',
                                           required_cols='SecurityId',
                                           expected_cols='NMV,Return'),
                         ['SecurityId', 'NMV', 'Return'])
        self.assertEqual(dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return',
                                           required_cols='SecurityId,NMV',
                                           expected_cols='NMV,Return,SecurityId'),
                         ['SecurityId', 'NMV', 'Return'])

        self.assertEqual(dbu._process_cols(available_cols='SecurityId,AxiomaId,BbergCode,NMV,Return',
                                           expected_cols='SecurityId,NMV'),
                         ['SecurityId', 'NMV'])

    def test_compile_sql_where_clauses(self):
        self.assertEqual(dbu.compile_sql_where_clause(), '')
        self.assertEqual(dbu.compile_sql_where_clause([]), '')
        self.assertEqual(dbu.compile_sql_where_clause("CountryCode IN ('US')"), "WHERE CountryCode IN ('US')")
        self.assertEqual(dbu.compile_sql_where_clause(['SecurityId IN (407,409)', 'FactorModelId=60']), 'WHERE SecurityId IN (407,409)\n\t\tAND FactorModelId=60')
        self.assertEqual(dbu.compile_sql_where_clause("EffectiveStartDate<='2021-09-23'||EffectiveEndDate>='2020-09-23'"), "WHERE EffectiveStartDate<='2021-09-23'\n\t\tAND EffectiveEndDate>='2020-09-23'")
        self.assertEqual(dbu.compile_sql_where_clause(['SecurityId IN (407,409)', 'FactorModelId=60', ' ']), 'WHERE SecurityId IN (407,409)\n\t\tAND FactorModelId=60')


if __name__ == '__main__':
    ut.main()
