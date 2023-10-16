from datetime import datetime

import numpy as np
import pandas as pd
import pandas.api.types as ptypes
from pytz import timezone

from fiddler import utils
from tests.fiddler.base import BaseTestCase

LOG = utils.logger.get_logger(__name__)


class TestUtils(BaseTestCase):
    def test_cleaning_df_with_all_datetime_col_should_convert_to_string_col(self):
        all_data = pd.DataFrame(
            {
                'a': [np.int64(1), np.int64(2)],
                'b': [np.uint8(1), np.uint8(2)],
                'c': [np.float128(1.1), np.float128(1.2)],
                'd': [np.bool_(True), np.bool_(False)],
                'e': [1, 2],
                'dates': [
                    datetime(2014, 5, 9),
                    datetime(2012, 6, 19),
                ],
            }
        )
        original_col_dtypes = all_data.dtypes.to_dict()
        utils.pandas_helper.clean_df_types(all_data)

        clean_col_dtypes = all_data.dtypes.to_dict()

        assert clean_col_dtypes['a'] == 'int'
        assert clean_col_dtypes['b'] in ['uint8', 'int8', 'int']
        assert clean_col_dtypes['c'] in ['float128', 'float']
        assert clean_col_dtypes['d'] == 'bool'
        assert clean_col_dtypes['e'] == 'int'
        assert original_col_dtypes['dates'] == 'datetime64[ns]'
        assert clean_col_dtypes['dates'] == 'string'

    def test_cleaning_df_with_all_datetime_string_col_should_convert_to_string_col(
        self,
    ):
        all_data = pd.DataFrame(
            {
                'a': [np.int64(1), np.int64(2)],
                'b': [np.uint8(1), np.uint8(2)],
                'c': [np.float128(1.1), np.float128(1.2)],
                'd': [np.bool_(True), np.bool_(False)],
                'e': [1, 2],
                'dates_string': [
                    '2021-07-19 23:59:58.790799',
                    '2021-07-19 23:59:58.790799',
                ],
                'mixed_dates_string': [
                    '2021-07-19 23:59:58.790799',
                    '2021-07-19 23:59',
                ],
                'empty_dates_string': [
                    '2021-07-19 23:59:58.790799',
                    '',
                ],
            }
        )
        original_col_dtypes = all_data.dtypes.to_dict()
        utils.pandas_helper.clean_df_types(all_data)

        clean_col_dtypes = all_data.dtypes.to_dict()

        assert clean_col_dtypes['a'] == 'int'
        assert clean_col_dtypes['b'] in ['uint8', 'int8', 'int']
        assert clean_col_dtypes['c'] in ['float128', 'float']
        assert clean_col_dtypes['d'] == 'bool'
        assert clean_col_dtypes['e'] == 'int'
        assert original_col_dtypes['dates_string'] == object
        assert original_col_dtypes['mixed_dates_string'] == object
        assert original_col_dtypes['empty_dates_string'] == object
        assert clean_col_dtypes['dates_string'] == 'string'
        assert clean_col_dtypes['mixed_dates_string'] == 'string'
        assert clean_col_dtypes['empty_dates_string'] == 'string'

    def test_cleaning_df_with_non_datetime_string_col_should_not_convert_to_string_col(
        self,
    ):
        all_data = pd.DataFrame(
            {
                'a': [np.int64(1), np.int64(2)],
                'b': [np.uint8(1), np.uint8(2)],
                'c': [np.float128(1.1), np.float128(1.2)],
                'd': [np.bool_(True), np.bool_(False)],
                'e': [1, 2],
                'random_string': [
                    'Test String',
                    'Random String',
                ],
            }
        )
        original_col_dtypes = all_data.dtypes.to_dict()
        utils.pandas_helper.clean_df_types(all_data)

        clean_col_dtypes = all_data.dtypes.to_dict()

        assert clean_col_dtypes['a'] == 'int'
        assert clean_col_dtypes['b'] in ['uint8', 'int8', 'int']
        assert clean_col_dtypes['c'] in ['float128', 'float']
        assert clean_col_dtypes['d'] == 'bool'
        assert clean_col_dtypes['e'] == 'int'
        assert original_col_dtypes['random_string'] == object
        assert clean_col_dtypes['random_string'] == object

    def test_cleaning_df_with_datetime_col_df_w_tz_should_convert_to_string_col(self):
        all_data = pd.DataFrame(
            {
                'a': [np.int64(1), np.int64(2)],
                'b': [np.uint8(1), np.uint8(2)],
                'c': [np.float128(1.1), np.float128(1.2)],
                'd': [np.bool_(True), np.bool_(False)],
                'e': [1, 2],
                'dates': [
                    datetime(2014, 5, 9),
                    datetime(2012, 6, 19),
                ],
            }
        )
        all_data['dates'] = pd.to_datetime(all_data['dates'], utc=True).dt.tz_convert(
            'UTC'
        )
        original_col_dtypes = all_data.dtypes.to_dict()
        # print(original_col_dtypes)
        utils.pandas_helper.clean_df_types(all_data)

        clean_col_dtypes = all_data.dtypes.to_dict()
        # print(clean_col_dtypes)
        assert clean_col_dtypes['a'] == 'int'
        assert clean_col_dtypes['b'] in ['uint8', 'int8', 'int']
        assert clean_col_dtypes['c'] in ['float128', 'float']
        assert clean_col_dtypes['d'] == 'bool'
        assert clean_col_dtypes['e'] == 'int'
        assert original_col_dtypes['dates'] == 'datetime64[ns, UTC]'
        assert clean_col_dtypes['dates'] == 'string'

    def test_cleaning_df_with_datetime_col_string_w_tz_should_convert_to_string_col(
        self,
    ):
        all_data = pd.DataFrame(
            {
                'a': [np.int64(1), np.int64(2)],
                'b': [np.uint8(1), np.uint8(2)],
                'c': [np.float128(1.1), np.float128(1.2)],
                'd': [np.bool_(True), np.bool_(False)],
                'e': [1, 2],
                'dates': [
                    datetime(2014, 5, 9, tzinfo=timezone('UTC')),
                    datetime(2012, 6, 19, tzinfo=timezone('GMT')),
                ],
            }
        )
        all_data['dates'] = pd.to_datetime(all_data['dates'], utc=True).dt.tz_convert(
            'UTC'
        )
        original_col_dtypes = all_data.dtypes.to_dict()

        utils.pandas_helper.clean_df_types(all_data)

        clean_col_dtypes = all_data.dtypes.to_dict()
        # print(clean_col_dtypes)
        assert clean_col_dtypes['a'] == 'int'
        assert clean_col_dtypes['b'] in ['uint8', 'int8', 'int']
        assert clean_col_dtypes['c'] in ['float128', 'float']
        assert clean_col_dtypes['d'] == 'bool'
        assert clean_col_dtypes['e'] == 'int'
        assert original_col_dtypes['dates'] == 'datetime64[ns, UTC]'
        assert clean_col_dtypes['dates'] == 'string'

    def test_try_series_retype(self):
        series = pd.Series([1, 2, 3], dtype='float')
        LOG.info('Recasting floating point array of ints to int.')
        series = utils.pandas_helper.try_series_retype(series, 'int')
        assert series.dtype == 'int'

        series = pd.Series([1, 2, None])
        LOG.info('Recasting floating point array of nullable ints to int.')
        series = utils.pandas_helper.try_series_retype(series, 'int')
        assert series.dtype == 'float'

    def test_try_series_retype_str_or_unkown(self):
        series = pd.Series(['HIGH', 'MEDIUM', '', None], dtype='str')
        LOG.info('Trying to recast a series of strings.')
        series = utils.pandas_helper.try_series_retype(series, 'str')
        assert ptypes.is_object_dtype(series)

    def test_try_series_retype_timestamp(self):
        series = pd.Series(
            ['2023-11-12 09:15:32.23', '2023-12-11 09:15:32.45'], dtype='str'
        )
        LOG.info('Trying to recast a series of timestamps.')
        series = utils.pandas_helper.try_series_retype(series, 'timestamp')
        assert series.dtype == 'datetime64[ns]'

    def test_try_series_retype_timestamp_error(self):
        series = pd.Series(['2023-11-12 09:15:32.23', None], dtype='str')

        LOG.info('Trying to recast a series of timestamps.')
        with self.assertRaises(TypeError):
            utils.pandas_helper.try_series_retype(series, 'timestamp')

    def test_is_datetime(self):
        series = pd.Series(
            ['2023-11-12 09:15:32.23', '2023-12-11 09:15:32.45'], dtype='str'
        )
        series = utils.pandas_helper.is_datetime(series)
        assert series is True

    def test_is_datetime_mixed(self):
        series = pd.Series(
            ['2023-11-12 09:15:32.23', '2023-12-11'], dtype='str'
        )
        series = utils.pandas_helper.is_datetime(series)
        assert series is True

    def test_is_datetime_wrong(self):
        series = pd.Series(
            ['2023-11-12 09:15:32.23', 'abcd'], dtype='str'
        )
        series = utils.pandas_helper.is_datetime(series)
        assert series is False
