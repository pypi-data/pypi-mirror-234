import numpy as np

import fiddler as fdl


def test_df_from_json_rows():
    """Tests the following:
    1. Column order in JSON different from in DatasetInfo
    2. Nullable integer values
    3. Categorical values not in possible values

    """
    dataset_info = fdl.DatasetInfo(
        display_name='test_dataset',
        columns=[
            fdl.Column('int_col', fdl.DataType.INTEGER),
            fdl.Column('nullable_int_col', fdl.DataType.INTEGER),
            fdl.Column(
                'categorical_col',
                fdl.DataType.CATEGORY,
                possible_values=['a', 'b', 'c'],
            ),
        ],
    )
    json_rows = [
        {'nullable_int_col': 1, 'categorical_col': 'a', 'int_col': 1},
        {'nullable_int_col': 2, 'categorical_col': 'b', 'int_col': 1},
        {'nullable_int_col': None, 'categorical_col': 'xyz', 'int_col': 2},
        {'nullable_int_col': 3, 'categorical_col': 'c', 'int_col': 3},
        {'nullable_int_col': None, 'categorical_col': 'a', 'int_col': 3},
    ]
    df = fdl.utils.df_from_json_rows(json_rows, dataset_info)
    # check column ordering follows from DatasetInfo
    assert df.columns.tolist() == ['int_col', 'nullable_int_col', 'categorical_col']
    # the fact that no errors were raised means we didn't fail on nullable
    # integers, but let's double check that things worked out nicely
    assert df['nullable_int_col'].dtype == 'float'
    assert not np.isnan(df.loc[0, 'nullable_int_col'])
    assert np.isnan(df.loc[2, 'nullable_int_col'])
    # check categories worked well
    assert df['categorical_col'].dtype == 'category'
    assert (
        df['categorical_col'].cat.categories.tolist()
        == dataset_info['categorical_col'].possible_values
    )
    assert np.isnan(df.loc[2, 'categorical_col'])
