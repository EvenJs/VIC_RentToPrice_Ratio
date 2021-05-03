import unittest
import sys
import os
import pandas as pd
from pandas.testing import assert_frame_equal

from src.vic_renttoprice_ratio.read_csv import read_csv_clean, read_house_price_csv, read_unit_price_csv, read_rent_csv

proj_dir = '../src/vic_renttoprice_ratio'
sys.path.append(os.path.join(proj_dir, 'vic_renttoprice_ratio'))


class MyTestCase (unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_csv_clean(self):
        df = pd.DataFrame(data=[['ABBOTSFORD', '123', '321'],
                                ['ABERFELDIE', '456', '654']],
                          columns=['NAME', '2020', '2019'])

        expected_df = pd.DataFrame(data=[['2020', 'ABBOTSFORD', '123'],
                                         ['2020', 'ABERFELDIE', '456'],
                                         ['2019', 'ABBOTSFORD', '321'],
                                         ['2019', 'ABERFELDIE', '654']],
                                   columns=['level_0', 'NAME', 0])
        tested_df = read_csv_clean(df)

        assert_frame_equal(expected_df, tested_df, check_dtype=False)

    def test_read_house_price_csv(self):
        raw_df = pd.DataFrame(data=[['ABBOTSFORD', '123', '123', '1', '2', '3', '4', ' '],
                                    ['ABERFELDIE', '123', '123', '1', '2', '3', '4', ' ']],
                              columns=['locality', '2018', '2019', 'prelim 2020', 'change', 'change.1', 'Growth PA',
                                       'Unnamed: 16'])

        expected_df = pd.DataFrame(data=[['2018', 'ABBOTSFORD', '123'],
                                         ['2018', 'ABERFELDIE', '123'],
                                         ['2019', 'ABBOTSFORD', '123'],
                                         ['2019', 'ABERFELDIE', '123'],
                                         ['2020', 'ABBOTSFORD', '1'],
                                         ['2020', 'ABERFELDIE', '1']],
                                   columns=['Year', 'NAME', 'House_Price'])

        test_df = read_house_price_csv(raw_df)
        self.assertEqual(6, len(test_df))
        self.assertEqual(3, test_df.shape[1])

        # assert_frame_equal(expected_df, test_df, check_dtype=False)

    def test_read_unit_price_csv(self):
        raw_df = pd.DataFrame (data=[['ABBOTSFORD', '123', '123', '123', '2', '3', '4', ' '],
                                     ['ABERFELDIE', '123', '123', '123', '2', '3', '4', ' ']],
                               columns=['locality', '2018', '2019', 'prelim 2020', 'change', 'change.1', 'Growth PA',
                                        'Unnamed: 16'])
        expected_df =pd.DataFrame(data=[['2018', 'ABBOTSFORD', '123'],
                                         ['2018', 'ABERFELDIE', '123'],
                                         ['2019', 'ABBOTSFORD', '123'],
                                         ['2019', 'ABERFELDIE', '123'],
                                         ['2020', 'ABBOTSFORD', '123'],
                                         ['2020', 'ABERFELDIE', '123']],
                                  columns=['Year', 'NAME', 'Unit_Price'])
        tested_df = read_unit_price_csv(raw_df)
        self.assertEqual(6, len(tested_df))
        self.assertEqual(3, tested_df.shape[1])
        assert_frame_equal(tested_df, expected_df, check_names=True, check_dtype=False)



if __name__ == '__main__':
    unittest.main()
